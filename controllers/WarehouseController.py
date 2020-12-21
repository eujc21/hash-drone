from database import hash_database
from models import warehouse_model
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

def getWarehouses():
    # This function pulls from the sqlite database the list of warehouse id data
    # This function also appends the list with the warehouse id if any are missing

    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    warehouse_list = []
    for wh in session.query(warehouse_model.WarehouseModel).all():
        warehouse_list.append(wh.getWarehouseId())
    return warehouse_list

def getWHLocation(id=0):
    # This function pulls from the sqlite database the warehouse location data
    # If requesting a certain warehouse id, an argument for the function would be your current
    # warehouse of concern to return the current warehouse of concern location data

    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    location = session.\
        query(warehouse_model.WarehouseModel).\
            filter(warehouse_model.WarehouseModel.warehouse_id == id).\
                first()
    # A function call to the warehouses location data under the warehouse model
    currentWh = location.getWarehouseLocation()
    return currentWh