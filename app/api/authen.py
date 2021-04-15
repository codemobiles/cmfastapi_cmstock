from datetime import datetime, timedelta

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.models.User import User as UserDB
router = APIRouter()


class User(BaseModel):
    username: str
    password: str
    level: Optional[str] = "normal"


@router.get("/")
def root():
    return {"iam": "authen"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username,
                     password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    return {"register": "ok"}


@router.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    try:
        db_user = db.query(UserDB).filter(
            UserDB.username == user.username).first()
        if not db_user:
            return {"login": "nok", "error": "invalid username"}
        if not verify_password(user.password, db_user.password):
            return {"login": "nok", "error": "invalid password"}

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires)
        return {"login": "ok", "token": token}
    except Exception as e:
        return {"login": "nok", "error": str(e)}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def hasAuthorized(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return False
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
        return False


@router.get("/items/")
async def read_own_items(isAuthorized: bool = Depends(hasAuthorized)):
    if isAuthorized:
        return [1, 2, 3]
    else:
        return {"Error": "Unauthorized"}
