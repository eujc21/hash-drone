from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrderModel(Base): # This class models the orders provided
    __tablename__ = "orders"    # Database table name
    __table_args__ = {"schema": "main"} # Argument calls (made from input file)

    id = Column(    # id with data type of model
        Integer,
        primary_key=True,
        nullable=False
    
    )
    dlx = Column(   # Order location x value and datatype
        Integer,
        nullable=False
    )
    
    dly = Column(   # Order location y value and datatype
        Integer,
        nullable=False
    )
    
    isDelivered = Column(   # Is the order delivered? boolean datatype mark value
        Boolean,
        nullable=False
    )
    
    def __repr__(self): # Fetch for the model id
        return '<Order model {}>'.format(self.id)

    def getId(self):    # Fetch for the order id for calls
        return self.id