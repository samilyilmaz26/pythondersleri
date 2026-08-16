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
        app.add_url_rule("/degiskenler", "variables", self.variables)

        app.add_url_rule(
            "/ogrenciler", "students", login_required(self.students)
        )
        app.add_url_rule(
            "/ogrenci/ekle",
            "add_student",
            login_required(self.add_student),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/ogrenci/sil/<int:id>", "delete_student", login_required(self.delete_student)
        )
        app.add_url_rule(
            "/ogrenci/guncelle/<int:id>",
            "update_student",
            login_required(self.update_student),
            methods=["GET", "POST"],
        )

        app.add_url_rule(
            "/login", "login", self.login, methods=["GET", "POST"]
        )
        app.add_url_rule("/logout", "logout", self.logout)
        app.add_url_rule(
            "/register", "register", self.register, methods=["GET", "POST"]
        )

        app.add_url_rule("/bolumler", "departments", login_required(self.departments))
        app.add_url_rule(
            "/bolum/ekle",
            "add_department",
            login_required(self.add_department),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/bolum/guncelle/<int:id>",
            "update_department",
            login_required(self.update_department),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/bolum/sil/<int:id>", "delete_department", login_required(self.delete_department)
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

    def variables(self):
        return render_template(
            "variables.html", **self.demo_data.as_template_context()
        )

    # ------------------------------------------------------------------
    # Students (Ogrenci)
    # ------------------------------------------------------------------
    def students(self):
        ogrenciler: list[Student] = self.student_repo.list_all()
        return render_template("students/student_list.html", ogrenciler=ogrenciler)

    def add_student(self):
        if request.method == "POST":
            student = Student.from_form(request.form)
            self.student_repo.add(student)
            flash("Öğrenci Ekleme Başarılı", "success")
            return redirect(url_for("students"))
        bolumler: list[Department] = self.department_repo.list_all()
        return render_template("students/add_student.html", bolumler=bolumler)

    def delete_student(self, id):
        self.student_repo.delete(id)
        flash("Öğrenci Silme Başarılı", "success")
        return redirect(url_for("students"))

    def update_student(self, id):
        ogrenci: Student = self.student_repo.find(id)

        if request.method == "POST":
            student = Student.from_form(request.form, id=id)
            self.student_repo.update(student)
            flash("Öğrenci Güncelleme Başarılı", "success")
            return redirect(url_for("students"))


        bolumler: list[Department] = self.department_repo.list_all()
        return render_template(
            "students/update_student.html", ogrenci=ogrenci, bolumler=bolumler
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
                return render_template("auth/login.html")

            if self.auth.attempt_login(username, password_entered):
                flash("Login Başarılı ...", "success")
                return redirect(url_for("index"))

            flash("Yanlış kullanıcı adı veya şifre", "danger")
        return render_template("auth/login.html")

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
                return render_template("auth/register.html")
            elif password != confirm:
                flash("Şifreler uyuşmuyor", "danger")
                return render_template("auth/register.html")

            self.auth.register(username, email, password)
            flash("Sisteme üye kaydı başarılı ", "success")
            return redirect(url_for("index"))
        return render_template("auth/register.html")

    # ------------------------------------------------------------------
    # Departments (Bolum)
    # ------------------------------------------------------------------
    def departments(self):
        bolumler: list[Department] = self.department_repo.list_all()
        return render_template("departments/department_list.html", bolumler=bolumler)

    def add_department(self):
        if request.method == "POST":
            department = Department(bolumad=request.form.get("bolumad"))
            self.department_repo.add(department)
            flash("Bölüm Ekleme Başarılı", "success")
            return redirect(url_for("departments"))
        return render_template("departments/add_department.html")

    def update_department(self, id):
        bolum: Department = self.department_repo.find(id)
        if request.method == "POST":
            department = Department(id=id, bolumad=request.form.get("bolumad"))
            self.department_repo.update(department)
            flash("Bölüm Güncelleme Başarılı", "success")
            return redirect(url_for("departments"))
        return render_template("departments/update_department.html", bolum=bolum)

    def delete_department(self, id):
        self.department_repo.delete(id)
        flash("Bölüm Silme Başarılı", "success")
        return redirect(url_for("departments"))

    # ------------------------------------------------------------------
    def run(self, debug=True):
        self.app.run(debug=debug)


if __name__ == "__main__":
    OgrenciOtomasyonApp().run()
