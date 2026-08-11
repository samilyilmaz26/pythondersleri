from flask import Flask, render_template, request, flash, redirect, url_for

from repo import StudentRepository, DepartmentRepository, UserRepository
from services import AuthService
from modules import DemoData
from models.student import Student
from models.department import Department


class OgrenciOtomasyonApp:
    """Student-automation Flask application, wrapped as a class.

    Repositories and services are created once in __init__ and reused
    by every route (they are effectively the app's dependencies),
    instead of the old style of importing module-level functions.
    """

    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

    def __init__(self, db_path="Ogrenci.db"):
        self.app = Flask(__name__)
        self.app.secret_key = self.SECRET_KEY

        self.student_repo = StudentRepository(db_path)
        self.department_repo = DepartmentRepository(db_path)
        self.user_repo = UserRepository(db_path)
        self.auth = AuthService(self.user_repo)
        self.demo_data = DemoData()

        self._register_routes()

    # ------------------------------------------------------------------
    # Route registration
    # ------------------------------------------------------------------
    def _register_routes(self):
        app = self.app
        login_required = self.auth.login_required

        app.add_url_rule("/", "index", self.index)
        app.add_url_rule("/about", "about", self.about)
        app.add_url_rule("/contact", "contact", self.contact)
        app.add_url_rule("/degiskenler", "degiskenler", self.degiskenler)

        app.add_url_rule(
            "/ogrenciler", "ogrenciler", login_required(self.ogrenciler)
        )
        app.add_url_rule(
            "/ogrenci/ekle",
            "ogrenci_ekle",
            login_required(self.ogrenci_ekle),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/ogrenci/sil/<int:id>", "ogrenci_sil", login_required(self.ogrenci_sil)
        )
        app.add_url_rule(
            "/ogrenci/guncelle/<int:id>",
            "ogrenci_guncelle",
            login_required(self.ogrenci_guncelle),
            methods=["GET", "POST"],
        )

        app.add_url_rule(
            "/login", "login", self.login, methods=["GET", "POST"]
        )
        app.add_url_rule("/logout", "logout", self.logout)
        app.add_url_rule(
            "/register", "register", self.register, methods=["GET", "POST"]
        )

        app.add_url_rule("/bolumler", "bolumler", login_required(self.bolumler))
        app.add_url_rule(
            "/bolum/ekle",
            "bolum_ekle",
            login_required(self.bolum_ekle),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/bolum/guncelle/<int:id>",
            "bolum_guncelle",
            login_required(self.bolum_guncelle),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/bolum/sil/<int:id>", "bolum_sil", login_required(self.bolum_sil)
        )

    # ------------------------------------------------------------------
    # Static pages
    # ------------------------------------------------------------------
    def index(self):
        return render_template("index.html")

    def about(self):
        return render_template("about.html")

    def contact(self):
        return render_template("contact.html")

    def degiskenler(self):
        return render_template(
            "degiskenler.html", **self.demo_data.as_template_context()
        )

    # ------------------------------------------------------------------
    # Students (Ogrenci)
    # ------------------------------------------------------------------
    def ogrenciler(self):
        ogrenciler: list[Student] = self.student_repo.list_all()
        return render_template("ogrencilist.html", ogrenciler=ogrenciler)

    def ogrenci_ekle(self):
        if request.method == "POST":
            ad = request.form.get("ad")
            soyad = request.form.get("soyad")
            bolumid = request.form.get("bolumid")
            self.student_repo.add(ad, soyad, bolumid)
            flash("Öğrenci Ekleme Başarılı", "success")
            return redirect(url_for("ogrenciler"))
        bolumler: list[Department] = self.department_repo.list_all()
        return render_template("ogrenciekle.html", bolumler=bolumler)

    def ogrenci_sil(self, id):
        self.student_repo.delete(id)
        flash("Öğrenci Silme Başarılı", "success")
        return redirect(url_for("ogrenciler"))

    def ogrenci_guncelle(self, id):
        ogrenci: Student = self.student_repo.find(id)

        if request.method == "POST":
            ad = request.form.get("ad")
            soyad = request.form.get("soyad")
            bolumid = request.form.get("bolumid")
            self.student_repo.update(id, ad, soyad, bolumid)
            flash("Öğrenci Güncelleme Başarılı", "success")
            return redirect(url_for("ogrenciler"))

        bolumler: list[Department] = self.department_repo.list_all()
        return render_template(
            "ogrenciguncelle.html", ogrenci=ogrenci, bolumler=bolumler
        )

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------
    def login(self):
        if request.method == "POST":
            username = request.form.get("username")
            password_entered = request.form.get("password")
            if not username or not password_entered:
                flash("Tüm alanları doldurun", "danger")
                return render_template("giris.html")

            if self.auth.attempt_login(username, password_entered):
                flash("Login Başarılı ...", "success")
                return redirect(url_for("index"))

            flash("Yanlış kullanıcı adı veya şifre", "danger")
        return render_template("giris.html")

    def logout(self):
        self.auth.logout()
        flash("Başarıyla çıkış yaptınız", "success")
        return redirect(url_for("index"))

    def register(self):
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            accept_tos = request.form.get("accept_tos")

            if not username or not email or not password or not confirm or not accept_tos:
                flash("Tüm Alanlar Doldurulmalı ", "danger")
                return render_template("kayit.html")
            elif password != confirm:
                flash("Şifreler uyuşmuyor", "danger")
                return render_template("kayit.html")

            self.auth.register(username, email, password)
            flash("Sisteme üye kaydı başarılı ", "success")
            return redirect(url_for("index"))
        return render_template("kayit.html")

    # ------------------------------------------------------------------
    # Departments (Bolum)
    # ------------------------------------------------------------------
    def bolumler(self):
        bolumler: list[Department] = self.department_repo.list_all()
        return render_template("bolumlist.html", bolumler=bolumler)

    def bolum_ekle(self):
        if request.method == "POST":
            bolumad = request.form.get("bolumad")
            self.department_repo.add(bolumad)
            flash("Bölüm Ekleme Başarılı", "success")
            return redirect(url_for("bolumler"))
        return render_template("bolumekle.html")

    def bolum_guncelle(self, id):
        bolum: Department = self.department_repo.find(id)
        if request.method == "POST":
            bolumad = request.form.get("bolumad")
            self.department_repo.update(id, bolumad)
            flash("Bölüm Güncelleme Başarılı", "success")
            return redirect(url_for("bolumler"))
        return render_template("bolumguncelle.html", bolum=bolum)

    def bolum_sil(self, id):
        self.department_repo.delete(id)
        flash("Bölüm Silme Başarılı", "success")
        return redirect(url_for("bolumler"))

    # ------------------------------------------------------------------
    def run(self, debug=True):
        self.app.run(debug=debug)


if __name__ == "__main__":
    OgrenciOtomasyonApp().run()
