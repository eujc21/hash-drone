from database import hash_database
from models import warehouse_model
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

def getWarehouses():
    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    warehouse_list = []
    for wh in session.query(warehouse_model.WarehouseModel).all():
        warehouse_list.append(wh.getWarehouseId())
    return warehouse_list

def getWHLocation(id=0):
    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    location = session.\
        query(warehouse_model.WarehouseModel).\
            filter(warehouse_model.WarehouseModel.warehouse_id == id).\
                first()
    currentWh = location.getWarehouseLocation()
    return currentWh