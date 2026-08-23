import asyncio
import os

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from clients.auth_client import AuthClient, UsernameTakenError
from clients.base_client import ServiceUnavailableError
from clients.city_client import CityClient
from clients.department_client import DepartmentClient
from clients.student_client import StudentClient
from clients.title_client import TitleClient
from services.auth_service import AuthService, NotLoggedInError

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "http://127.0.0.1:8001")
DEPARTMENT_SERVICE_URL = os.environ.get("DEPARTMENT_SERVICE_URL", "http://127.0.0.1:8002")
CITY_SERVICE_URL = os.environ.get("CITY_SERVICE_URL", "http://127.0.0.1:8003")
TITLE_SERVICE_URL = os.environ.get("TITLE_SERVICE_URL", "http://127.0.0.1:8004")
STUDENT_SERVICE_URL = os.environ.get("STUDENT_SERVICE_URL", "http://127.0.0.1:8005")
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")

auth_client = AuthClient(AUTH_SERVICE_URL)
auth = AuthService(auth_client)
department_client = DepartmentClient(DEPARTMENT_SERVICE_URL)
city_client = CityClient(CITY_SERVICE_URL)
title_client = TitleClient(TITLE_SERVICE_URL)
student_client = StudentClient(STUDENT_SERVICE_URL)


async def login_required(request: Request):
    auth.require_login(request)


@app.exception_handler(NotLoggedInError)
async def handle_not_logged_in(request: Request, exc: NotLoggedInError):
    flash(request, "Bu sayfaya gitmek için giriş yapmalısınız", "danger")
    return RedirectResponse(url="/login", status_code=303)


@app.exception_handler(ServiceUnavailableError)
async def handle_service_unavailable(request: Request, exc: ServiceUnavailableError):
    flash(request, "Bir servise şu anda ulaşılamıyor, lütfen daha sonra tekrar deneyin", "danger")
    return RedirectResponse(url="/", status_code=303)


def flash(request: Request, message: str, category: str = "info"):
    flashes = request.session.get("flashes", [])
    flashes.append({"message": message, "category": category})
    request.session["flashes"] = flashes


def pop_flashes(request: Request):
    flashes = request.session.get("flashes", [])
    request.session["flashes"] = []
    return flashes


def flashed_messages_processor(request: Request):
    return {"get_flashed_messages": lambda: pop_flashes(request)}


templates = Jinja2Templates(directory="templates", context_processors=[flashed_messages_processor])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "home.html")


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request, "about.html")


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse(request, "auth/login.html")


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        logged_in = await auth.attempt_login(request, username, password)
    except ServiceUnavailableError:
        flash(request, "Auth servisine şu anda ulaşılamıyor", "danger")
        return templates.TemplateResponse(request, "auth/login.html")

    if logged_in:
        flash(request, "Giriş başarılı", "success")
        return RedirectResponse(url="/", status_code=303)

    flash(request, "Kullanıcı adı veya şifre hatalı", "danger")
    return templates.TemplateResponse(request, "auth/login.html")


@app.get("/logout")
async def logout(request: Request):
    auth.logout(request)
    flash(request, "Başarıyla çıkış yaptınız", "success")
    return RedirectResponse(url="/", status_code=303)


@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse(request, "auth/register.html")


@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm: str = Form(...),
):
    if password != confirm:
        flash(request, "Şifreler uyuşmuyor", "danger")
        return templates.TemplateResponse(request, "auth/register.html")

    try:
        await auth.register(username, email, password)
    except UsernameTakenError:
        flash(request, "Bu kullanıcı adı zaten kayıtlı", "danger")
        return templates.TemplateResponse(request, "auth/register.html")
    except ServiceUnavailableError:
        flash(request, "Auth servisine şu anda ulaşılamıyor", "danger")
        return templates.TemplateResponse(request, "auth/register.html")

    flash(request, "Kayıt başarılı, giriş yapabilirsiniz", "success")
    return RedirectResponse(url="/login", status_code=303)


@app.get("/departments", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def departments(request: Request):
    bolumler = await department_client.list_all()
    return templates.TemplateResponse(request, "departments/department_list.html", {"departments": bolumler})


@app.get("/departments/add", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def add_department_form(request: Request):
    return templates.TemplateResponse(request, "departments/add_department.html")


@app.post("/departments/add", dependencies=[Depends(login_required)])
async def add_department(request: Request, name: str = Form(...)):
    await department_client.add(name)
    flash(request, "Bölüm ekleme başarılı", "success")
    return RedirectResponse(url="/departments", status_code=303)


@app.get("/departments/update/{id}", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def update_department_form(request: Request, id: int):
    department = await department_client.find(id)
    return templates.TemplateResponse(request, "departments/update_department.html", {"department": department})


@app.post("/departments/update/{id}", dependencies=[Depends(login_required)])
async def update_department(request: Request, id: int, name: str = Form(...)):
    await department_client.update(id, name)
    flash(request, "Bölüm güncelleme başarılı", "success")
    return RedirectResponse(url="/departments", status_code=303)


@app.get("/departments/delete/{id}", dependencies=[Depends(login_required)])
async def delete_department(request: Request, id: int):
    await department_client.delete(id)
    flash(request, "Bölüm silme başarılı", "success")
    return RedirectResponse(url="/departments", status_code=303)


@app.get("/cities", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def cities(request: Request):
    sehirler = await city_client.list_all()
    return templates.TemplateResponse(request, "cities/city_list.html", {"cities": sehirler})


@app.get("/cities/add", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def add_city_form(request: Request):
    return templates.TemplateResponse(request, "cities/add_city.html")


@app.post("/cities/add", dependencies=[Depends(login_required)])
async def add_city(request: Request, name: str = Form(...)):
    await city_client.add(name)
    flash(request, "Şehir ekleme başarılı", "success")
    return RedirectResponse(url="/cities", status_code=303)


@app.get("/cities/update/{id}", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def update_city_form(request: Request, id: int):
    city = await city_client.find(id)
    return templates.TemplateResponse(request, "cities/update_city.html", {"city": city})


@app.post("/cities/update/{id}", dependencies=[Depends(login_required)])
async def update_city(request: Request, id: int, name: str = Form(...)):
    await city_client.update(id, name)
    flash(request, "Şehir güncelleme başarılı", "success")
    return RedirectResponse(url="/cities", status_code=303)


@app.get("/cities/delete/{id}", dependencies=[Depends(login_required)])
async def delete_city(request: Request, id: int):
    await city_client.delete(id)
    flash(request, "Şehir silme başarılı", "success")
    return RedirectResponse(url="/cities", status_code=303)

@app.get("/titles", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def titles(request: Request):
    unvanlar = await title_client.list_all()
    return templates.TemplateResponse(request, "titles/title_list.html", {"titles": unvanlar})


@app.get("/titles/add", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def add_title_form(request: Request):
    return templates.TemplateResponse(request, "titles/add_title.html")


@app.post("/titles/add", dependencies=[Depends(login_required)])
async def add_title(request: Request, name: str = Form(...)):
    await title_client.add(name)
    flash(request, "Unvan ekleme başarılı", "success")
    return RedirectResponse(url="/titles", status_code=303)


@app.get("/titles/update/{id}", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def update_title_form(request: Request, id: int):
    title = await title_client.find(id)
    return templates.TemplateResponse(request, "titles/update_title.html", {"title": title})


@app.post("/titles/update/{id}", dependencies=[Depends(login_required)])
async def update_title(request: Request, id: int, name: str = Form(...)):
    await title_client.update(id, name)
    flash(request, "Unvan güncelleme başarılı", "success")
    return RedirectResponse(url="/titles", status_code=303)


@app.get("/titles/delete/{id}", dependencies=[Depends(login_required)])
async def delete_title(request: Request, id: int):
    await title_client.delete(id)
    flash(request, "Unvan silme başarılı", "success")
    return RedirectResponse(url="/titles", status_code=303)


async def _students_with_labels() -> list[dict]:
    ogrenciler, sehirler, bolumler = await asyncio.gather(
        student_client.list_all(), city_client.list_all(), department_client.list_all()
    )
    city_names = {c["id"]: c["name"] for c in sehirler}
    department_names = {d["id"]: d["name"] for d in bolumler}
    for student in ogrenciler:
        student["cityname"] = city_names.get(student.get("cityid"))
        student["departmentname"] = department_names.get(student.get("departmentid"))
    return ogrenciler


@app.get("/students", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def students(request: Request):
    ogrenciler = await _students_with_labels()
    return templates.TemplateResponse(request, "students/student_list.html", {"students": ogrenciler})


@app.get("/students/add", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def add_student_form(request: Request):
    sehirler = await city_client.list_all()
    bolumler = await department_client.list_all()
    return templates.TemplateResponse(
        request, "students/add_student.html", {"cities": sehirler, "departments": bolumler}
    )


@app.post("/students/add", dependencies=[Depends(login_required)])
async def add_student(
    request: Request,
    name: str = Form(...),
    surname: str = Form(""),
    street: str = Form(""),
    number: str = Form(""),
    cityid: str = Form(""),
    departmentid: str = Form(""),
):
    await student_client.add(
        name, surname, street, number, int(cityid) if cityid else None, int(departmentid) if departmentid else None
    )
    flash(request, "Öğrenci ekleme başarılı", "success")
    return RedirectResponse(url="/students", status_code=303)


@app.get("/students/update/{id}", response_class=HTMLResponse, dependencies=[Depends(login_required)])
async def update_student_form(request: Request, id: int):
    student, sehirler, bolumler = await asyncio.gather(
        student_client.find(id), city_client.list_all(), department_client.list_all()
    )
    return templates.TemplateResponse(
        request, "students/update_student.html", {"student": student, "cities": sehirler, "departments": bolumler}
    )


@app.post("/students/update/{id}", dependencies=[Depends(login_required)])
async def update_student(
    request: Request,
    id: int,
    name: str = Form(...),
    surname: str = Form(""),
    street: str = Form(""),
    number: str = Form(""),
    cityid: str = Form(""),
    departmentid: str = Form(""),
):
    await student_client.update(
        id, name, surname, street, number, int(cityid) if cityid else None, int(departmentid) if departmentid else None
    )
    flash(request, "Öğrenci güncelleme başarılı", "success")
    return RedirectResponse(url="/students", status_code=303)


@app.get("/students/delete/{id}", dependencies=[Depends(login_required)])
async def delete_student(request: Request, id: int):
    await student_client.delete(id)
    flash(request, "Öğrenci silme başarılı", "success")
    return RedirectResponse(url="/students", status_code=303)
