import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from .database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    total = Column(Float)
    paid = Column(Float)
    change = Column(Float)
    payment_type = Column(String(200))
    payment_detail = Column(String(2000))
    order_list = Column(String(2000))
    staff_id = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
