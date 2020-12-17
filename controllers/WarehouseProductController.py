from database import *
from models import WarehouseProductModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

def getWareHouseProductQty(warehouse_id=0, product_id=0):
    dbms = HashDataBase(SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    product_qty = session.query(WarehouseProductModel).\
        filter(WarehouseProductModel.warehouse_id == warehouse_id).\
        filter(WarehouseProductModel.product_id == product_id).\
            first()
    product_qty = product_qty.getQty()
    return product_qty
