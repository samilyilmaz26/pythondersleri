import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from events import publish_event
from repo.department_repository import DepartmentRepository

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "departments.db"
DB_PATH = os.environ.get("DB_PATH", str(DEFAULT_DB_PATH))

repo = DepartmentRepository(DB_PATH)

app = FastAPI(title="Department Service")


class DepartmentIn(BaseModel):
    name: str


class DepartmentOut(BaseModel):
    id: int
    name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/departments", response_model=list[DepartmentOut])
def list_departments():
    return [DepartmentOut(**d.to_dict()) for d in repo.list_all()]


@app.get("/departments/{id}", response_model=DepartmentOut)
def get_department(id: int):
    department = repo.find(id)
    if department is None:
        raise HTTPException(status_code=404, detail="not found")
    return DepartmentOut(**department.to_dict())


@app.post("/departments", response_model=DepartmentOut, status_code=201)
def create_department(data: DepartmentIn):
    new_id = repo.add(data.name)
    publish_event("department.created", {"id": new_id, "name": data.name})
    return DepartmentOut(id=new_id, name=data.name)


@app.put("/departments/{id}", response_model=DepartmentOut)
def update_department(id: int, data: DepartmentIn):
    if repo.find(id) is None:
        raise HTTPException(status_code=404, detail="not found")
    repo.update(id, data.name)
    publish_event("department.updated", {"id": id, "name": data.name})
    return DepartmentOut(id=id, name=data.name)


@app.delete("/departments/{id}", status_code=204)
def delete_department(id: int):
    repo.delete(id)
    publish_event("department.deleted", {"id": id})
