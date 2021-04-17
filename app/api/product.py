import datetime
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.api import security
from app.models.Product import Product as ProductDB
from app.db import get_db
from sqlalchemy.orm import Session
from app.api import schema
import shutil
from pathlib import Path

router = APIRouter()


@router.get("/")
async def get_product(db: Session = Depends(get_db), isAuthorized: bool = Depends(security.hasAuthorized)):
    if isAuthorized:
        try:
            products = db.query(ProductDB)
            return products.all()
        except Exception as e:
            return {"product": "nok", "error": str(e)}
    else:
        return {"Error": "Unauthorized"}


@router.get("/{id}")
async def get_product_by_id(id: str, db: Session = Depends(get_db), isAuthorized: bool = Depends(security.hasAuthorized)):
    if isAuthorized:
        try:
            product = db.query(ProductDB).filter(ProductDB.id == id).first()
            return product
        except Exception as e:
            return {"product": "nok", "error": str(e)}
    else:
        return {"Error": "Unauthorized"}


@router.post("/")
async def insert_product(product: schema.Product, db: Session = Depends(get_db), isAuthorized: bool = Depends(security.hasAuthorized)):
    if isAuthorized:
        try:
            db_product = ProductDB(**product.dict())
            db.add(db_product)
            db.commit()
            return {"result": "ok"}
        except Exception as e:
            return {"product": "nok", "error": str(e)}
    else:
        return {"Error": "Unauthorized"}


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


@router.post("/files")
async def create_file(image: UploadFile = File(...), token: str = Form(...), db: Session = Depends(get_db)):
    try:
        save_upload_file(image, Path(
            "/Users/chaiyasit/Desktop/Training/python_training/cmfastapi_cmstock/app/uploaded/images/test.jpg"))
        return {
            "token": token
        }
    except Exception as e:
        return {"product": "nok", "error": str(e)}


@router.put("/")
async def insert_product(product: schema.Product, db: Session = Depends(get_db), isAuthorized: bool = Depends(security.hasAuthorized)):
    if isAuthorized:
        try:
            product_db = db.query(ProductDB).filter(
                ProductDB.id == product.id)
            product_db.update({ProductDB.name: product.name,
                              ProductDB.price: product.price,
                              ProductDB.stock: product.stock})
            db.commit()
            return {"result": "ok"}
        except Exception as e:
            return {"product": "nok", "error": str(e)}
    else:
        return {"Error": "Unauthorized"}


@router.delete("/{id}")
async def delete_product(id: str, db: Session = Depends(get_db), isAuthorized: bool = Depends(security.hasAuthorized)):
    if isAuthorized:
        try:
            products = db.query(ProductDB).filter(ProductDB.id == id)
            products.delete()
            db.commit()
            return {"result": "ok"}
        except Exception as e:
            return {"product": "nok", "error": str(e)}
    else:
        return {"Error": "Unauthorized"}
