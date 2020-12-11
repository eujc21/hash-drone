from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from . import product_model, warehouse_model

Base = declarative_base()

class WarehouseProductModel(Base):
    __tablename__ = "warehouse_products"
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
    
    warehouse_id = Column(
        Integer,
        ForeignKey(warehouse_model.WarehouseModel.warehouse_id),
        nullable=False
    )
    
    qty = Column(
        Integer,
        nullable=False
    )
    
    def __repr__(self):
        return '<OrderProduct model {}>'.format(self.id)