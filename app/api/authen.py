from datetime import datetime, timedelta

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.api import security
from app.api import schema
from app.models.User import User as UserDB
router = APIRouter()


@router.get("/")
def root():
    return {"iam": "authen"}


@router.post("/register")
def register(user: schema.User, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username,
                     password=security.get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    return {"register": "ok"}


@router.post("/login")
def login(user: schema.User, db: Session = Depends(get_db)):
    try:
        db_user = db.query(UserDB).filter(
            UserDB.username == user.username).first()
        if not db_user:
            return {"login": "nok", "error": "invalid username"}
        if not security.verify_password(user.password, db_user.password):
            return {"login": "nok", "error": "invalid password"}

        access_token_expires = timedelta(
            minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = security.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires)
        return {"login": "ok", "token": token}
    except Exception as e:
        return {"login": "nok", "error": str(e)}
