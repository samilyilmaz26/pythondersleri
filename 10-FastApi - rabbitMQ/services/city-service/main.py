import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from events import publish_event
from repo.city_repository import CityRepository

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "cities.db"
DB_PATH = os.environ.get("DB_PATH", str(DEFAULT_DB_PATH))

repo = CityRepository(DB_PATH)

app = FastAPI(title="City Service")


class CityIn(BaseModel):
    name: str


class CityOut(BaseModel):
    id: int
    name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/cities", response_model=list[CityOut])
def list_cities():
    return [CityOut(**c.to_dict()) for c in repo.list_all()]


@app.get("/cities/{id}", response_model=CityOut)
def get_city(id: int):
    city = repo.find(id)
    if city is None:
        raise HTTPException(status_code=404, detail="not found")
    return CityOut(**city.to_dict())


@app.post("/cities", response_model=CityOut, status_code=201)
def create_city(data: CityIn):
    new_id = repo.add(data.name)
    publish_event("city.created", {"id": new_id, "name": data.name})
    return CityOut(id=new_id, name=data.name)


@app.put("/cities/{id}", response_model=CityOut)
def update_city(id: int, data: CityIn):
    if repo.find(id) is None:
        raise HTTPException(status_code=404, detail="not found")
    repo.update(id, data.name)
    publish_event("city.updated", {"id": id, "name": data.name})
    return CityOut(id=id, name=data.name)


@app.delete("/cities/{id}", status_code=204)
def delete_city(id: int):
    repo.delete(id)
    publish_event("city.deleted", {"id": id})
