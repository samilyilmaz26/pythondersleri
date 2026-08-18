import os

from flask import Flask, render_template, request, flash, redirect, url_for

from clients import (
    AuthClient,
    DepartmentClient,
    TitleClient,
    StudentClient,
    InstructorClient,
    ServiceUnavailableError,
)
from services import AuthService
from modules import DemoData
from models.student import Student
from models.instructor import Instructor


class OgrenciOtomasyonGateway:
    """Web gateway for the student-automation microservices.

    Renders the same Jinja UI the old monolith did and owns the Flask
    session (login state), but never touches a database directly —
    every domain operation is an HTTP call to the matching backend
    service. Cross-domain view data (department/title names on
    student and instructor rows) is composed here instead of via SQL
    JOINs, since each backend service only knows its own table.
    """

    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = self.SECRET_KEY

        self.department_client = DepartmentClient(
            os.environ.get("DEPARTMENT_SERVICE_URL", "http://localhost:5002")
        )
        self.title_client = TitleClient(os.environ.get("TITLE_SERVICE_URL", "http://localhost:5003"))
        self.student_client = StudentClient(os.environ.get("STUDENT_SERVICE_URL", "http://localhost:5004"))
        self.instructor_client = InstructorClient(
            os.environ.get("INSTRUCTOR_SERVICE_URL", "http://localhost:5005")
        )
        self.auth_client = AuthClient(os.environ.get("AUTH_SERVICE_URL", "http://localhost:5001"))

        self.auth = AuthService(self.auth_client)
        self.demo_data = DemoData()

        self.app.register_error_handler(ServiceUnavailableError, self.handle_service_unavailable)

        self._register_routes()

    def handle_service_unavailable(self, error):
        flash("Bir servise şu anda ulaşılamıyor, lütfen daha sonra tekrar deneyin", "danger")
        return redirect(url_for("index"))

    # ------------------------------------------------------------------
    # Route registration
    # ------------------------------------------------------------------
    def _register_routes(self):
        app = self.app
        login_required = self.auth.login_required

        app.add_url_rule("/", "index", self.index)
        app.add_url_rule("/about", "about", self.about)
        app.add_url_rule("/contact", "contact", self.contact)
        app.add_url_rule("/variables", "variables", self.variables)

        app.add_url_rule(
            "/students", "students", login_required(self.students)
        )
        app.add_url_rule(
            "/students/add",
            "add_student",
            login_required(self.add_student),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/students/delete/<int:id>", "delete_student", login_required(self.delete_student)
        )
        app.add_url_rule(
            "/students/update/<int:id>",
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

        app.add_url_rule("/departments", "departments", login_required(self.departments))
        app.add_url_rule(
            "/departments/add",
            "add_department",
            login_required(self.add_department),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/departments/update/<int:id>",
            "update_department",
            login_required(self.update_department),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/departments/delete/<int:id>", "delete_department", login_required(self.delete_department)
        )

        app.add_url_rule(
            "/instructors", "instructors", login_required(self.instructors)
        )
        app.add_url_rule(
            "/instructors/add",
            "add_instructor",
            login_required(self.add_instructor),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/instructors/delete/<int:id>", "delete_instructor", login_required(self.delete_instructor)
        )
        app.add_url_rule(
            "/instructors/update/<int:id>",
            "update_instructor",
            login_required(self.update_instructor),
            methods=["GET", "POST"],
        )

        app.add_url_rule("/titles", "titles", login_required(self.titles))
        app.add_url_rule(
            "/titles/add",
            "add_title",
            login_required(self.add_title),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/titles/update/<int:id>",
            "update_title",
            login_required(self.update_title),
            methods=["GET", "POST"],
        )
        app.add_url_rule(
            "/titles/delete/<int:id>", "delete_title", login_required(self.delete_title)
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
    # Students (Ogrenci) — student-service + department-service
    # ------------------------------------------------------------------
    def students(self):
        raw_students = self.student_client.list_all()
        departments = {d["id"]: d["bolumad"] for d in self.department_client.list_all()}
        ogrenciler = []
        for data in raw_students:
            data["bolumad"] = departments.get(data["bolumid"])
            ogrenciler.append(Student.from_row(data))
        return render_template("students/student_list.html", ogrenciler=ogrenciler)

    def add_student(self):
        if request.method == "POST":
            student = Student.from_form(request.form)
            self.student_client.add(student.to_dict())
            flash("Öğrenci Ekleme Başarılı", "success")
            return redirect(url_for("students"))
        bolumler = self.department_client.list_all()
        return render_template("students/add_student.html", bolumler=bolumler)

    def delete_student(self, id):
        self.student_client.delete(id)
        flash("Öğrenci Silme Başarılı", "success")
        return redirect(url_for("students"))

    def update_student(self, id):
        ogrenci = Student.from_row(self.student_client.find(id))

        if request.method == "POST":
            student = Student.from_form(request.form, id=id)
            self.student_client.update(id, student.to_dict())
            flash("Öğrenci Güncelleme Başarılı", "success")
            return redirect(url_for("students"))

        bolumler = self.department_client.list_all()
        return render_template(
            "students/update_student.html", ogrenci=ogrenci, bolumler=bolumler
        )

    # ------------------------------------------------------------------
    # Auth — auth-service
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
    # Departments (Bolum) — department-service
    # ------------------------------------------------------------------
    def departments(self):
        bolumler = self.department_client.list_all()
        return render_template("departments/department_list.html", bolumler=bolumler)

    def add_department(self):
        if request.method == "POST":
            self.department_client.add(request.form.get("bolumad"))
            flash("Bölüm Ekleme Başarılı", "success")
            return redirect(url_for("departments"))
        return render_template("departments/add_department.html")

    def update_department(self, id):
        bolum = self.department_client.find(id)
        if request.method == "POST":
            self.department_client.update(id, request.form.get("bolumad"))
            flash("Bölüm Güncelleme Başarılı", "success")
            return redirect(url_for("departments"))
        return render_template("departments/update_department.html", bolum=bolum)

    def delete_department(self, id):
        self.department_client.delete(id)
        flash("Bölüm Silme Başarılı", "success")
        return redirect(url_for("departments"))

    # ------------------------------------------------------------------
    # Instructors (Egitmen) — instructor-service + department/title-service
    # ------------------------------------------------------------------
    def instructors(self):
        raw_instructors = self.instructor_client.list_all()
        departments = {d["id"]: d["bolumad"] for d in self.department_client.list_all()}
        titles = {t["id"]: t["unvanad"] for t in self.title_client.list_all()}
        egitmenler = []
        for data in raw_instructors:
            data["bolumad"] = departments.get(data["bolumid"])
            data["unvanad"] = titles.get(data["unvanid"])
            egitmenler.append(Instructor.from_row(data))
        return render_template("instructors/instructor_list.html", egitmenler=egitmenler)

    def add_instructor(self):
        if request.method == "POST":
            instructor = Instructor.from_form(request.form)
            self.instructor_client.add(instructor.to_dict())
            flash("Eğitmen Ekleme Başarılı", "success")
            return redirect(url_for("instructors"))
        bolumler = self.department_client.list_all()
        unvanlar = self.title_client.list_all()
        return render_template(
            "instructors/add_instructor.html", bolumler=bolumler, unvanlar=unvanlar
        )

    def delete_instructor(self, id):
        self.instructor_client.delete(id)
        flash("Eğitmen Silme Başarılı", "success")
        return redirect(url_for("instructors"))

    def update_instructor(self, id):
        egitmen = Instructor.from_row(self.instructor_client.find(id))

        if request.method == "POST":
            instructor = Instructor.from_form(request.form, id=id)
            self.instructor_client.update(id, instructor.to_dict())
            flash("Eğitmen Güncelleme Başarılı", "success")
            return redirect(url_for("instructors"))

        bolumler = self.department_client.list_all()
        unvanlar = self.title_client.list_all()
        return render_template(
            "instructors/update_instructor.html",
            egitmen=egitmen,
            bolumler=bolumler,
            unvanlar=unvanlar,
        )

    # ------------------------------------------------------------------
    # Titles (Unvan) — title-service
    # ------------------------------------------------------------------
    def titles(self):
        unvanlar = self.title_client.list_all()
        return render_template("titles/title_list.html", unvanlar=unvanlar)

    def add_title(self):
        if request.method == "POST":
            self.title_client.add(request.form.get("unvanad"))
            flash("Unvan Ekleme Başarılı", "success")
            return redirect(url_for("titles"))
        return render_template("titles/add_title.html")

    def update_title(self, id):
        unvan = self.title_client.find(id)
        if request.method == "POST":
            self.title_client.update(id, request.form.get("unvanad"))
            flash("Unvan Güncelleme Başarılı", "success")
            return redirect(url_for("titles"))
        return render_template("titles/update_title.html", unvan=unvan)

    def delete_title(self, id):
        self.title_client.delete(id)
        flash("Unvan Silme Başarılı", "success")
        return redirect(url_for("titles"))

    # ------------------------------------------------------------------
    def run(self, debug=True):
        self.app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=debug)


if __name__ == "__main__":
    OgrenciOtomasyonGateway().run(debug=os.environ.get("FLASK_DEBUG", "1") == "1")
