from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from . import product_model, order_model

Base = declarative_base()

class OrderProductModel(Base):
    __tablename__ = "order_products"
    __table_args__ = {"schema": "main"}

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    product_id = Column(
        Integer,
        ForeignKey(product_model.ProductModel.product_id),
        nullable=False
    )
    
    order_id = Column(
        Integer,
        ForeignKey(order_model.OrderModel.id),
        nullable=False
    )
    
    qty = Column(
        Integer,
        nullable=False
    )
    
    def __repr__(self):
        return '<OrderProduct model {}>'.format(self.id)