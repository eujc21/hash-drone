from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrderModel(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "main"}

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    dlx = Column(
        Integer,
        nullable=False
    )
    
    dly = Column(
        Integer,
        nullable=False
    )
    
    isDelivered = Column(
        Boolean,
        nullable=False
    )
    
    def __repr__(self):
        return '<Order model {}>'.format(self.id)

    def getId(self):
        return self.id