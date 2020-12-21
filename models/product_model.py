from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductModel(Base):   # This class models the products provided
    """Data model example."""
    __tablename__ = "products"  # Database table name
    __table_args__ = {"schema": "main"} # Argument calls (made from input file)

    id = Column(    # id of the product model and datatype
        Integer,
        primary_key=True,
        nullable=False
    )
    product_id = Column(    # id of the product (product type) and datatype
        String(100),
        nullable=False
    )
    product_weight = Column(    # product weight and datatype
        Float,
        nullable=False
    )

    def __repr__(self): # Fetch for product model id
        return '<Product model {}>'.format(self.id)
