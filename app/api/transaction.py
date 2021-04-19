import datetime
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.api import security
from app.models.Transaction import Transaction as TransactionDB
from app.db import get_db
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.api import schema
import shutil
from pathlib import Path
import os

router = APIRouter()


@router.get("/")
async def get_transaction(db: Session = Depends(get_db)):
    transactions = db.query(TransactionDB).order_by(desc("created_at"))
    return transactions.all()


def get_transaction_form(
        id: Optional[str] = Form(None),
        total: float = Form(...),
        paid: float = Form(...),
        change: float = Form(...),
        payment_type: str = Form(...),
        payment_detail: str = Form(...),
        order_list: str = Form(...)):
    return schema.Transaction(id=id,
                              total=total,
                              paid=paid,
                              change=change,
                              payment_type=payment_type,
                              payment_detail=payment_detail,
                              order_list=order_list,
                              staff_id=staff_id)


@ router.post("/")
async def insert_transaction(transaction: schema.Transaction,
                             db: Session = Depends(get_db)):
    try:
        db_transaction = TransactionDB(**transaction.dict())
        db.add(db_transaction)
        db.commit()
        return {"result"}
    except Exception as e:
        return {"transaction": "nok", "error": str(e)}
