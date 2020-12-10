from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WarehouseModel(Base):
    __tablename__ = "warehouses"
    __table_args__ = {"schema": "main"}

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    
    warehouse_id = Column(
        Integer,
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
    
    def __repr__(self):
        return '<WareHouse model {}>'.format(self.id)