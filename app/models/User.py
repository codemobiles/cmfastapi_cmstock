import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(100))
    level = Column(String(100), default="normal")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
