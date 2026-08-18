# Öğrenci Otomasyonu — Microservices

Bu sürüm, tek bir Flask uygulaması + tek SQLite dosyasından oluşan OOP
monolitin (bkz. `7-Ogrenciotomasyonu-OOP`) **tam mikroservis** mimarisine
dönüştürülmüş halidir. Her alan (auth, bölüm, unvan, öğrenci, eğitmen)
kendi veritabanına ve JSON REST API'sine sahip bağımsız bir Flask servisi;
mevcut Jinja arayüzü ve oturum tabanlı girişi koruyan ince bir web-gateway
bu servislere HTTP üzerinden bağlanır.

## Mimari

```
web-gateway (Flask, port 5000, dışa açık)
  - Jinja şablonları, Bootstrap layout, flash mesajları
  - Giriş durumu (session) SADECE burada tutulur
  - HTTP client'lar servisleri çağırır ve görünüm verisini birleştirir
      |         |            |            |              |
      v         v            v            v              v
  auth-svc  department-svc  title-svc  student-svc   instructor-svc
  (5001)    (5002)          (5003)     (5004)        (5005)
  users.db  departments.db  titles.db  students.db   instructors.db
```

Backend servisleri saf CRUD JSON API'leridir; birbirlerini hiç çağırmazlar.
Örneğin `student-service` sadece `bolumid`'yi saklar, bölüm adını asla
sorgulamaz — öğrenci/eğitmen listelerinde görünen `bolumad`/`unvanad`
alanları **web-gateway** tarafından, ilgili servislerin listelerini çekip
Python içinde birleştirerek (API composition) oluşturulur. Bu sayede
servisler birbirinden tamamen bağımsız kalır.

`auth-service` şifre hash'lemeyi (`passlib sha256_crypt`) kendi içinde yapar;
gateway sadece kullanıcı adı/şifreyi iletir ve başarılı girişte kendi
Flask session'ını kurar — session state hâlâ tek bir yerde, gateway'de.

## Klasör yapısı

```
services/
  auth-service/         -> User tablosu, POST /auth/login, POST /auth/register
  department-service/   -> Bolum tablosu, GET/POST/PUT/DELETE /departments
  title-service/        -> Unvan tablosu, GET/POST/PUT/DELETE /titles
  student-service/      -> Ogrenci tablosu, GET/POST/PUT/DELETE /students
  instructor-service/   -> Egitmen tablosu, GET/POST/PUT/DELETE /instructors
                            (Instructor hâlâ Student'tan miras alıyor)
web-gateway/
  app.py                -> route'lar + client çağrıları + veri birleştirme
  clients/               -> her servis için ince bir requests sarmalayıcısı
  services/auth_service.py -> session/login_required, auth_client'a delege eder
  templates/              -> değişmedi (aynı Jinja şablonları)
scripts/
  migrate_split_db.py    -> eski Ogrenci.db'yi 5 ayrı .db dosyasına böler
data/                    -> migrasyon sonrası üretilen .db dosyaları (docker volume)
docker-compose.yml          -> üretim/temel yapılandırma (kod image'a gömülü, FLASK_DEBUG=0)
docker-compose.override.yml -> sadece geliştirme: kod bind-mount + FLASK_DEBUG=1, `up` ile otomatik uygulanır
```

Her servis kendi `database.py` (bağlantı context manager'ı), `models/`
(`BaseModel` tabanlı) ve `repo/` (`BaseRepository` tabanlı) kopyasını taşır;
bu küçük dosyaların servisler arasında tekrarlanması, servislerin
birbirinden bağımsız deploy edilebilmesinin bilinçli bedelidir.

## Çalıştırma (Docker Compose)

İlk kurulumda, veritabanı dosyaları henüz yokken bir kere çalıştırılması
gereken adım:

```bash
python scripts/migrate_split_db.py   # sadece ilk kurulumda: data/*.db üretir
```

Bu script eski `Ogrenci.db`'yi `data/*.db` dosyalarına böler. `data/`
klasörü zaten doluysa (ör. daha önce bir kez çalıştırdıysan) tekrar
çalıştırmana gerek yok.

### Geliştirme ortamı (kod değiştikçe otomatik reload)

`docker-compose.override.yml`, `docker-compose.yml` ile **otomatik**
birleşir (Compose'un varsayılan davranışı budur), servis kodunu konteynere
canlı mount eder ve Flask'ın debug/reloader modunu açar. Yani:

```bash
docker compose up --build   # ilk seferinde veya requirements.txt değişince
docker compose up           # sadece Python/HTML kodu değiştiyse yeterli
```

Bundan sonra `services/*/app.py`, `models/`, `repo/` veya
`web-gateway/templates/` içinde yaptığın değişiklikler, dosyayı kaydettiğin
anda ilgili konteynerde otomatik olarak yansır (Flask reloader süreci
yeniden başlatır) — konteynerleri yeniden build etmen gerekmez.
`--build`'i sadece `requirements.txt` değiştiğinde veya Dockerfile'da bir
değişiklik yaptığında tekrar kullanman yeterli.

### Üretim / canlı ortam

Canlı ortamda kod host'tan mount edilmemeli ve Flask debug modu kapalı
olmalı (`docker-compose.yml` içinde her servis için `FLASK_DEBUG: 0`
zaten ayarlı). Override dosyasının otomatik birleşmesini engellemek için
`-f` ile açıkça sadece `docker-compose.yml`'i belirt:

```bash
docker compose -f docker-compose.yml up --build -d
```

Kodda değişiklik yaptıktan sonra canlıya almak için bu komutu (özellikle
`--build`'i) tekrar çalıştırman gerekir; çünkü üretimde kod image'ın içine
gömülüdür, host'tan canlı mount edilmez.

Gateway `http://localhost:5000` üzerinden açılır; diğer 5 servis sadece
konteyner ağı içinde erişilebilir (host'a port açmazlar).

## Yerel çalıştırma (Docker'sız)

Her servis bağımsız bir Flask uygulamasıdır, `PORT` ve `DB_PATH` ortam
değişkenleriyle yapılandırılır:

```bash
PORT=5002 DB_PATH=../../data/departments.db python services/department-service/app.py
# ... diğer 4 servis için de aynı şekilde ...
AUTH_SERVICE_URL=http://localhost:5001 DEPARTMENT_SERVICE_URL=http://localhost:5002 \
TITLE_SERVICE_URL=http://localhost:5003 STUDENT_SERVICE_URL=http://localhost:5004 \
INSTRUCTOR_SERVICE_URL=http://localhost:5005 python web-gateway/app.py
```

## Davranış notu

Eski monolitte öğrenci/eğitmen listeleri `INNER JOIN` kullandığından
`bolumid`/`unvanid` alanı boş olan kayıtlar listeden tamamen düşüyordu.
Mikroservis sürümünde her servis kendi tablosunu olduğu gibi döndürüyor;
gateway eşleşen bir bölüm/unvan bulamazsa sadece `bolumad`/`unvanad`'ı boş
bırakıyor, kaydı listeden gizlemiyor.
