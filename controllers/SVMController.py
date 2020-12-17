from database import hash_database
from models import OrderModel, ProductModel, OrderProductModel, WarehouseProductModel
from controllers import WarehouseProductController, WarehouseController
from util import distance
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from sqlalchemy.sql import label

def getSVMTable(warehouse_id):
    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    svmtable = []
    warehouse_location = WarehouseController.getWHLocation(warehouse_id)
    print(warehouse_location)
    distinct_ids = session.query(OrderModel.id).distinct()
    for op in distinct_ids:
        obj = {}
        obj["order_id"] = op[0]
        for order_id in op:
            order = session.query(OrderModel).filter(OrderModel.id == order_id).first()
            obj["order_location_x"] = order.dlx
            obj["order_location_y"] = order.dly
            order_results = session.query(OrderProductModel).filter(OrderProductModel.order_id == order_id).all()
            # order_results = session.query(OrderProductModel).all()
            obj["has_all_available_products"] = []
            for result in order_results:
                qty = result.getQty()
                wh_qty = WarehouseProductController.getWareHouseProductQty(warehouse_id, result.product_id)
                obj["inventory_product_"+str(result.product_id)+"_qty"] = wh_qty
                obj["product_"+str(result.product_id)+"_qty"] = qty
                obj["has_all_available_products"].append(True if qty == wh_qty else False)
            obj["has_all_available_products"] = all(obj["has_all_available_products"])
            obj["warehouse_location_x"] = warehouse_location["wh_location_x"]
            obj["warehouse_location_y"] = warehouse_location["wh_location_y"]
            obj["distance_from_warehouse"] = distance(
                {
                    0: obj["warehouse_location_x"],
                    1: obj["warehouse_location_y"]
                },
                {
                    0: obj["order_location_x"],
                    1: obj["order_location_y"]
                }
             )
        svmtable.append(obj)
    return svmtable
