from database import hash_database
from models import OrderModel, ProductModel, OrderProductModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from sqlalchemy.sql import label

def getSVMTable():
    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    svmtable = []
    for op in session.query(OrderModel.id).distinct():
        obj = {}
        obj["order_id"] = op[0]
        for order_id in op:
            order = session.query(OrderModel).filter(OrderModel.id == order_id).first()
            obj["order_location_x"] = order.dlx
            obj["order_location_y"] = order.dly

            for item in session.query(OrderProductModel).\
                filter(OrderProductModel.order_id == order_id).\
                all():
                obj["product_"+str(item.id)+"_qty"] = item.qty,
        svmtable.append(obj)
    return svmtable
