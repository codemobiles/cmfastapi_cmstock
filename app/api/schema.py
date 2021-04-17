from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    level: Optional[str] = "normal"


class Product(BaseModel):
    id: Optional[str] = None
    name: str
    stock: int
    price: float
    image: str
    created_at: Optional[str] = None
