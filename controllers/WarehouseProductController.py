from database import *
from models import WarehouseProductModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

def getWareHouseProductQty(warehouse_id=0, product_id=0):
    # This function pulls from the sqlite database the products of each warehouse
    # arguments for this function would be a warehouse id for what warehouse you are focuses on
    # and a product id for how many of that product exist in the warehouse

    dbms = HashDataBase(SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    product_qty = session.query(WarehouseProductModel).\
        filter(WarehouseProductModel.warehouse_id == warehouse_id).\
        filter(WarehouseProductModel.product_id == product_id).\
            first()
    product_qty = product_qty.getQty()  # A function call to the product's qty under the product model
    return product_qty
