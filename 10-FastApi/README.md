# Öğrenci Otomasyonu — Mikroservisler + RabbitMQ/CQRS

FastAPI ile yazılmış, her biri kendi SQLite veritabanına sahip bağımsız mikroservislerden oluşan bir öğrenci otomasyon sistemi. `web-gateway` bu servislerin önünde tek bir HTML arayüzü sunar.

## Servisler

| Servis | Port (container içi) | Sorumluluk |
|---|---|---|
| `user-service` | 8001 | Kullanıcı/kimlik doğrulama |
| `department-service` | 8002 | Bölümler |
| `city-service` | 8003 | Şehirler |
| `title-service` | 8004 | Unvanlar |
| `student-service` | 8005 | Öğrenciler |
| `web-gateway` | 8000 (host'a açık) | HTML arayüz, tüm servisleri birleştirir |
| `rabbitmq` | 5672 / 15672 (host'a açık) | Servisler arası event mesajlaşması |

## Neden RabbitMQ / CQRS?

Başlangıçta `/students` sayfası her istekte `student-service`, `city-service` ve `department-service`'e senkron HTTP çağrısı yapıp sonucu gateway kodunda Python'da birleştiriyordu (`_students_with_labels`). Bu, öğrenci sayısı büyüdükçe (örn. 100.000 kayıt) limitsiz DB sorgusu + üç ayrı HTTP/JSON round-trip + cache'sizlik + sayfalamasız render yüzünden ciddi bir performans sorunu oluşturuyordu.

Çözüm olarak **CQRS read-model** deseni uygulandı:

- Yazma tarafı (student/city/department servisleri) değişmeden kalır, her create/update/delete'te RabbitMQ'ya bir **event** yayınlar.
- `web-gateway` içinde, bu event'leri dinleyen bir **consumer**, önceden join'lenmiş/denormalize edilmiş bir `student_read_model` tablosunu günceller.
- `/students` artık hiçbir servise gitmeden, doğrudan bu yerel tablodan **sayfalı** okur — maliyet öğrenci sayısından bağımsız, sabit.

```
student-service ──┐
city-service ──────┼──► RabbitMQ (domain.events, topic exchange) ──► web-gateway consumer ──► student_read_model (SQLite)
department-service ┘                                                                                  ▲
                                                                                                        │
                                                                              /students  ───────────────┘  (sayfalı okuma, sayfalama)
```

## Event akışı

**Exchange:** `domain.events` (topic, durable)
**Queue:** `student-read-model-queue` (durable), routing key binding'leri: `student.*`, `city.created/updated/deleted`, `department.created/updated/deleted`

| Event | Consumer davranışı |
|---|---|
| `student.created` / `student.updated` | lookup tablosundan cityname/departmentname çekilir, `student_read_model` upsert edilir |
| `student.deleted` | ilgili satır `student_read_model`'den silinir |
| `city.created` / `city.updated` | `city_lookup` güncellenir + o şehre bağlı **tüm** öğrenci satırlarında `cityname` cascade güncellenir |
| `city.deleted` | `city_lookup`'tan silinir + bağlı öğrencilerde `cityname` NULL'lanır |
| `department.created` / `department.updated` | `department_lookup` güncellenir + cascade `departmentname` güncellemesi |
| `department.deleted` | `department_lookup`'tan silinir + bağlı öğrencilerde `departmentname` NULL'lanır |

Yazma işlemleri (`/students/add`, `/students/update`, `/students/delete`) hâlâ `student-service`'e HTTP isteği atar — read-model'e doğrudan yazılmaz. Event RabbitMQ üzerinden işlenene kadar kısa bir **eventual consistency** penceresi vardır (pratikte ~1 saniyenin altında).

## Başlangıç senkronizasyonu (backfill)

Gateway her açıldığında, consumer'ı başlatmadan önce 3 kaynak servisten tam bir liste çekip `student_read_model` ve lookup tablolarını senkronize eden bir **backfill** çalışır:

- Event sisteminden önce oluşturulmuş kayıtları doldurur.
- Kaynak serviste artık var olmayan (downtime sırasında silinmiş, event kaçırılmış) "zombi" satırları temizler.
- Idempotent'tir, her restart'ta güvenle tekrar çalışır — sistem kendi kendini kaynakla tutarlı hale getirir (self-healing).

## Yeni dosyalar (web-gateway)

```
web-gateway/
  database.py                          # SQLite connection context manager
  events_consumer.py                   # RabbitMQ consumer (aio-pika)
  backfill.py                          # İlk senkronizasyon
  models/
    base_model.py
    student_read_model.py
  repo/
    base_repository.py
    student_read_model_repository.py   # create_table, upsert/bulk_upsert, delete/bulk_delete, cascade update, list_paginated
    lookup_repository.py               # city_lookup / department_lookup
```

`student-service`, `city-service`, `department-service` içine de `events.py` (senkron `pika` ile publish) eklendi ve create/update/delete endpoint'leri event yayınlayacak şekilde güncellendi.

## Çalıştırma

```
docker compose up -d --build
```

- Uygulama: http://localhost:8000
- RabbitMQ yönetim paneli: http://localhost:15672 (guest / guest)

## Ölçekte doğrulama (100.000 öğrenci ile load test)

- `/students?page=1`: **~25-29ms** (yeni mimari) vs **~2907ms** (eski `_students_with_labels` yaklaşımı - 3 servise senkron HTTP + Python'da join)
- Backfill, `bulk_upsert`/`bulk_delete` sayesinde tek transaction'da çalışır - başlangıçta bunun yerine öğrenci başına ayrı SQLite bağlantısı açan bir sürüm 100k satırda süresiz kilitlenmişti.
- Backfill'in kendi HTTP client'larının timeout'u 30s'ye çıkarıldı (interaktif isteklerde kullanılanlar 3s'de kalıyor) çünkü 100k satırlık `/students` yanıtı (~12MB JSON) ~2.6 saniye sürüyor.

## Bilinen sınırlamalar

- `guest`/`guest` sadece geliştirme ortamı için uygundur; üretimde `RABBITMQ_DEFAULT_USER`/`RABBITMQ_DEFAULT_PASS` ile ayrı kullanıcı tanımlanmalı.
- Eventual consistency nedeniyle bir yazma işleminden hemen sonraki milisaniyelerde `/students` eski veriyi gösterebilir.
- `title-service` şu an event sistemine dahil değil (öğrenci read-model'inde kullanılmıyor).
- Sayfalama `LIMIT/OFFSET` kullanıyor: `offset` büyüdükçe (çok derin sayfalarda) sorgu yavaşlar (offset=100000'de ~450ms). Kalıcı çözüm keyset/cursor pagination'a geçmek olur, ama bu "sayfa numarasına git" UX'ini değiştirir - şu an uygulanmadı.
- `student_read_model_repository.count()` metodu hâlâ mevcut ama `/students` tarafından **çağrılmıyor** - `COUNT(*)` SQLite'ta O(n) olduğu için her istekte çağrılması 100k satırda ~500ms'lik gizli bir maliyet ekliyordu; bunun yerine "Sonraki" linki dönen satır sayısına bakılarak gösteriliyor.

## Adım adım geliştirme notları

Bu entegrasyonun nasıl adım adım kurulduğu (`1-rabbitMQ.txt` … `8-rabbitMQ.txt`) proje kök dizininde referans olarak duruyor.
