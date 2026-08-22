import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from repo.title_repository import TitleRepository

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "titles.db"
DB_PATH = os.environ.get("DB_PATH", str(DEFAULT_DB_PATH))

repo = TitleRepository(DB_PATH)

app = FastAPI(title="Title Service")


class TitleIn(BaseModel):
    name: str


class TitleOut(BaseModel):
    id: int
    name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/titles", response_model=list[TitleOut])
def list_titles():
    return [TitleOut(**t.to_dict()) for t in repo.list_all()]


@app.get("/titles/{id}", response_model=TitleOut)
def get_title(id: int):
    title = repo.find(id)
    if title is None:
        raise HTTPException(status_code=404, detail="not found")
    return TitleOut(**title.to_dict())


@app.post("/titles", response_model=TitleOut, status_code=201)
def create_title(data: TitleIn):
    new_id = repo.add(data.name)
    return TitleOut(id=new_id, name=data.name)


@app.put("/titles/{id}", response_model=TitleOut)
def update_title(id: int, data: TitleIn):
    if repo.find(id) is None:
        raise HTTPException(status_code=404, detail="not found")
    repo.update(id, data.name)
    return TitleOut(id=id, name=data.name)


@app.delete("/titles/{id}", status_code=204)
def delete_title(id: int):
    repo.delete(id)
