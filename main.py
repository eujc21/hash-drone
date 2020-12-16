from database import hash_database
from models import ProductModel, OrderModel,OrderProductModel, WarehouseModel, WarehouseProductModel
from controllers import OrderController, SVMController, WarehouseController
from sqlalchemy.orm import sessionmaker
import os
from util.seeder import read_file

def setupDB():
    num_rows, num_columns, num_drones, max_time, max_cargo, products, wh_list, order_list, order_product, wh_products = read_file('./assets/busy_day.in')
    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')
    dbms.create_db_tables()
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    for product in products:
        session.add(ProductModel(**product))
    for order in order_list:
        session.add(OrderModel(**order))
    for order in order_product:
        # session.add(order_product_model.OrderModel(**order))
        order_id = order["order_id"]
        for key in dict(order["items"]).keys():
            order["items"][key]
            session.add(
                OrderProductModel(
                    **{
                        "order_id":order_id,
                        "product_id": key,
                        "qty": order["items"][key]
                    }
                )
            )
    for warehouse in wh_list:
        session.add(WarehouseModel(**warehouse))

    for wh_product in wh_products:
        session.add(WarehouseProductModel(**wh_product))
    session.commit()

    
def trainsvm():
    values = SVMController.getSVMTable()
    group_value = []
    for value in values:
        print(values)
    #for wh in WarehouseController.getWarehouses():
#        print(WarehouseController.getWHLocation(wh))
    return False

def simulation():
    return False

def main():
    if os.path.exists('./hash.sqlite'):
        os.remove('./hash.sqlite')
    else:
        print("Can not delete the file as it doesn't exists")
    if os.path.exists('./text.txt'):
        os.remove('./text.txt')
    else:
        print("Can not delete the file as it doesn't exists")
    setupDB()
    trainsvm()
    simulation()
    

if __name__ == "__main__": main()
