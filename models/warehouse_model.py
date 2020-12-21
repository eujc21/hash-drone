from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WarehouseModel(Base): # This class models the warehouses provided
    __tablename__ = "warehouses"    # Database table name
    __table_args__ = {"schema": "main"} # Argument calls (made from input file)

    id = Column(    # model id and datatype
        Integer,
        primary_key=True,
        nullable=False
    )

    warehouse_id = Column(  # Warehouse id and datatype
        Integer,
        nullable=False
    )

    dlx = Column(   # Warehouse location x value and datatype
        Integer,
        nullable=False
    )
    
    dly = Column(   # Warehouse location y value and datatype
        Integer,
        nullable=False
    )
    
    def __repr__(self): # Fetch for warehouse model id
        return '<Warehouse model {}>'.format(self.id)
    
    def getWarehouseId(self):   # Fetch for warehouse id
        return self.warehouse_id

    def getWarehouseLocation(self): # Fetch for warehouse location values
        return {"wh_location_x":self.dlx, "wh_location_y":self.dly}
