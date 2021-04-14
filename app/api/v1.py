from fastapi import APIRouter
from app.api import authen, product, transaction

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models import database


engine = create_engine("sqlite:///./cmstock.db")
database.Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

api_router = APIRouter()
api_router.include_router(authen.router, prefix="/authen", tags=["authen"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(
    transaction.router, prefix="/transaction", tags=["transaction"])