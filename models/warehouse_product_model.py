from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from . import product_model, warehouse_model

Base = declarative_base()

class WarehouseProductModel(Base):    # This class models the warehouse's products provided
    __tablename__ = "warehouse_products"    # Database table name
    __table_args__ = {"schema": "main"} # Argument calls (made from input file)

    id = Column(    # model id and datatype
        Integer,
        primary_key=True,
        nullable=False
    )
    product_id = Column(    # product id(type) and datatype, fetches from product_model file
        Integer,
        ForeignKey(product_model.ProductModel.product_id),
        nullable=False
    )
    
    warehouse_id = Column(  # warehouse id and datatype, fetches from warehouse_model file
        Integer,
        ForeignKey(warehouse_model.WarehouseModel.warehouse_id),
        nullable=False
    )
    
    qty = Column(
        Integer,
        nullable=False
    )
    
    def __repr__(self):
        return '<WareHouseProduct model {}>'.format(self.id)
    
    def getQty(self):
        return self.qty