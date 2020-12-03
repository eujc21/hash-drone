from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductModel(Base):
    """Data model example."""
    __tablename__ = "products"
    __table_args__ = {"schema": "main"}

    id = Column(
        Integer,
        primary_key=True,
        nullable=False
    )
    product_id = Column(
        String(100),
        nullable=False
    )
    # description = Column(
    #     Text,
    #     nullable=True
    # )
    # join_date = Column(
    #     DateTime,
    #     nullable=False
    # )
    # vip = Column(
    #     Boolean,
    #     nullable=False
    # )
    product_weight = Column(
        Float,
        nullable=False
    )
    # data = Column(
    #     PickleType,
    #     nullable=False
    # )

    def __repr__(self):
        return '<Product model {}>'.format(self.id)
