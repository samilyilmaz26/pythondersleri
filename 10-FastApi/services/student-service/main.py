import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from events import publish_event
from repo.student_repository import StudentRepository

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "students.db"
DB_PATH = os.environ.get("DB_PATH", str(DEFAULT_DB_PATH))

repo = StudentRepository(DB_PATH)

app = FastAPI(title="Student Service")


class StudentIn(BaseModel):
    name: str
    surname: str | None = None
    street: str | None = None
    number: str | None = None
    cityid: int | None = None
    departmentid: int | None = None


class StudentOut(BaseModel):
    id: int
    name: str
    surname: str | None = None
    street: str | None = None
    number: str | None = None
    cityid: int | None = None
    departmentid: int | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/students", response_model=list[StudentOut])
def list_students():
    return [StudentOut(**s.to_dict()) for s in repo.list_all()]


@app.get("/students/{id}", response_model=StudentOut)
def get_student(id: int):
    student = repo.find(id)
    if student is None:
        raise HTTPException(status_code=404, detail="not found")
    return StudentOut(**student.to_dict())


@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(data: StudentIn):
    new_id = repo.add(data.name, data.surname, data.street, data.number, data.cityid, data.departmentid)
    publish_event("student.created", {"id": new_id, **data.model_dump()})
    return StudentOut(id=new_id, **data.model_dump())


@app.put("/students/{id}", response_model=StudentOut)
def update_student(id: int, data: StudentIn):
    if repo.find(id) is None:
        raise HTTPException(status_code=404, detail="not found")
    repo.update(id, data.name, data.surname, data.street, data.number, data.cityid, data.departmentid)
    publish_event("student.updated", {"id": id, **data.model_dump()})
    return StudentOut(id=id, **data.model_dump())


@app.delete("/students/{id}", status_code=204)
def delete_student(id: int):
    repo.delete(id)
    publish_event("student.deleted", {"id": id})
