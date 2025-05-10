from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.now)
    payment_method = Column(String(50), nullable=False)
    status = Column(String(20), default='pending')
    reference = Column(String(100), unique=True)
    description = Column(String(200))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, status={self.status})>" 