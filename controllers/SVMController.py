from database import hash_database
from models import order_model, product_model, order_product_model
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

def getSVMTable():
    dbms = hash_database.HashDatabse(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    svmtable = []
    for op, i, j in session.query(order_product_model.OrderProductModel, product_model.ProductModel, order_model.OrderModel).\
            filter(order_product_model.OrderProductModel.order_id == order_model.OrderModel.id).\
            filter(order_product_model.OrderProductModel.product_id == product_model.ProductModel.product_id).\
            all():
            svmobject = {
                "order_id": op.order_id,                
                "product_"+str(op.product_id)+"_qty": op.qty,
                "order_location_x": j.dlx,
                "order_location_y": j.dly,
            }
            svmtable.append(svmobject)
            
    return svmtable
