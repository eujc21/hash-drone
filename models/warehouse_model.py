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
        return '<Warehouse model {}>'.format(self.id)
    
    def getWarehouseId(self):
        return self.warehouse_id

    def getWarehouseLocation(self):
        return {"wh_location_x":self.dlx, "wh_location_y":self.dly}
