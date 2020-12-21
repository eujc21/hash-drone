from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .order_model import OrderModel
from .product_model import ProductModel

Base = declarative_base()

class OrderProductModel(Base): # This class models the order's products provided
    __tablename__ = "order_products"    # Database table name
    __table_args__ = {"schema": "main"} # Argument calls (made from input file)

    id = Column(    # id and datatype of model
        Integer,
        primary_key=True,
        nullable=False
    )
    product_id = Column(    # product type(id) and data type, fetches from product_model file
        Integer,
        ForeignKey(ProductModel.product_id),
        nullable=False
    )
    
    order_id = Column(  # order id and datatype, fetches from order_model file
        Integer,
        ForeignKey(OrderModel.id),
        nullable=False
    )
    
    qty = Column(   # qty of product in order and datatype
        Integer,
        nullable=False
    )

    # order = relationship(OrderModel,
    #     primaryjoin='OrderProductModel.order_id==OrderModel.id',
    #     join_depth=3,
    #     lazy='joined'
    # )    
    def __repr__(self): # Fetch for model id
        return '<OrderProduct model {}>'.format(self.id)

    def getQty(self):   # Fetch for qty of product in order
        return self.qty
