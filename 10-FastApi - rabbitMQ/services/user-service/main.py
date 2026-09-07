import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel

from repo.user_repository import UserRepository

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "users.db"
DB_PATH = os.environ.get("DB_PATH", str(DEFAULT_DB_PATH))

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
repo = UserRepository(DB_PATH)

app = FastAPI(title="User Service")


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/register", response_model=UserOut, status_code=201)
def register(data: RegisterRequest):
    if repo.find_by_username(data.username):
        raise HTTPException(status_code=409, detail="username already exists")

    hashed_password = pwd_context.hash(data.password)
    new_id = repo.register(data.username, data.email, hashed_password)
    return UserOut(id=new_id, username=data.username, email=data.email)


@app.post("/auth/login", response_model=UserOut)
def login(data: LoginRequest):
    user = repo.find_by_username(data.username)
    if user and pwd_context.verify(data.password, user.password):
        return UserOut(id=user.id, username=user.username, email=user.email)
    raise HTTPException(status_code=401, detail="invalid credentials")
