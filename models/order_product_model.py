from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .order_model import OrderModel
from .product_model import ProductModel

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
        ForeignKey(ProductModel.product_id),
        nullable=False
    )
    
    order_id = Column(
        Integer,
        ForeignKey(OrderModel.id),
        nullable=False
    )
    
    qty = Column(
        Integer,
        nullable=False
    )

    # order = relationship(OrderModel,
    #     primaryjoin='OrderProductModel.order_id==OrderModel.id',
    #     join_depth=3,
    #     lazy='joined'
    # )    
    def __repr__(self):
        return '<OrderProduct model {}>'.format(self.id)

#    def getValue(self, key):
#        return self[key]