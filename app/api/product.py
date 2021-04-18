import datetime
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.api import security
from app.models.Product import Product as ProductDB
from app.db import get_db
from sqlalchemy.orm import Session
from app.api import schema
import shutil
from pathlib import Path
import os

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


def save_upload_file(upload_file: UploadFile, id: str) -> str:
    try:
        fileName = "{}.jpg".format(id)
        dest = Path(os.getcwd() + "/uploaded/images/{}".format(fileName))
        with dest.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        return fileName
    finally:
        upload_file.file.close()


def delete_upload_file(fileName: str) -> None:
    filePath = os.getcwd() + "/uploaded/images/{}".format(fileName)
    if os.path.exists(filePath):
        os.remove(filePath)


def get_product_form(
        id: Optional[str] = Form(...),
        name: str = Form(...),
        price: float = Form(...),
        stock: int = Form(...)):
    return schema.Product(id=id, name=name, price=price, stock=stock, image="")


@router.post("/")
async def insert_product(product: schema.Product = Depends(get_product_form),
                         image: UploadFile = File(...),
                         db: Session = Depends(get_db)):
    try:
        db_product = ProductDB(**product.dict())
        db.add(db_product)
        db.commit()

        # Update image name in db
        if image:
            fileName = save_upload_file(image, db_product.id)
            product_db = db.query(ProductDB).filter(
                ProductDB.id == db_product.id)
            product_db.update({ProductDB.image: fileName})
            db.commit()

        return {"result"}

    except Exception as e:
        return {"product": "nok", "error": str(e)}


@router.put("/")
async def update_product(product: schema.Product = Depends(get_product_form),
                         image: Optional[UploadFile] = File(None),
                         db: Session = Depends(get_db),
                         isAuthorized: bool = Depends(security.hasAuthorized)):
    if isAuthorized:
        try:
            product_db = db.query(ProductDB).filter(ProductDB.id == product.id)
            product_db.update({ProductDB.name: product.name,
                               ProductDB.price: product.price,
                               ProductDB.stock: product.stock})
            db.commit()

            # Update image name in db
            if image:
                fileName = save_upload_file(image, product.id)
            return {"result": "ok"}
        except Exception as e:
            return {"product": "nok", "error": str(e)}

        return {"Error": "Unauthorized"}


@router.delete("/{id}")
async def delete_product(id: str, db: Session = Depends(get_db), isAuthorized: bool = Depends(security.hasAuthorized)):
    if isAuthorized:
        try:
            products = db.query(ProductDB).filter(ProductDB.id == id)
            imageFile = products.first().image
            print("delete image", imageFile)
            delete_upload_file(imageFile)
            products.delete()
            db.commit()
            return {"result": "ok"}
        except Exception as e:
            return {"product": "nok", "error": str(e)}
    else:
        return {"Error": "Unauthorized"}
