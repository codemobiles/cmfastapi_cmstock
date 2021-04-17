import datetime
from fastapi import APIRouter, Depends
from app.api import security
from app.models.Product import Product as ProductDB
from app.db import get_db
from sqlalchemy.orm import Session
from app.api import schema
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


@router.delete("/{id}")
async def delete_product(id: str, db: Session = Depends(get_db), isAuthorized: bool = Depends(security.hasAuthorized)):
    if isAuthorized:
        try:
            product = db.query(ProductDB).filter(ProductDB.id == id).first()
            product.delete()
            db.commit()
            return {"result": "ok"}
        except Exception as e:
            return {"product": "nok", "error": str(e)}
    else:
        return {"Error": "Unauthorized"}
