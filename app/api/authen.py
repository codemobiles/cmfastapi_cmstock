from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.User import User as UserDB

router = APIRouter()


class User(BaseModel):
    username: str
    password: str
    level: Optional[str] = "normal"


@router.get("/")
def root():
    return {"iam": "authen"}


@router.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    return {"register": "ok"}
