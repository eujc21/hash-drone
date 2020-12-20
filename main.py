import os
from database import hash_database
from models import ProductModel, OrderModel,OrderProductModel, WarehouseModel, WarehouseProductModel
from controllers import OrderController, SVMController, WarehouseController, WarehouseProductController
from sqlalchemy.orm import sessionmaker
from util.seeder import read_file
import pandas as pd

def setupDB():
    num_rows, num_columns, num_drones, max_time, max_cargo, products, wh_list, order_list, order_product, warehouse_products = read_file('./assets/busy_day.in')
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

    for wh_product in warehouse_products:
        for wh_pr in wh_product:
            session.add(WarehouseProductModel(**wh_pr))
    session.commit()

    
def createCSV():
    warehouses = WarehouseController.getWarehouses()
    # warehouse_id= input("Which warehouse would you like to train on , pick 0-9: ")

    # for warehouse_id in warehouses:
    for warehouse_id in warehouses:
        svmTable = SVMController.getSVMTable(warehouse_id)
        group_value = []
        for value in svmTable:
            group_value.append(value)
        df = pd.DataFrame(group_value)
        df.fillna(0, inplace=True)
        gfg_csv_data = df.to_csv('./assets/warehouse_'+str(warehouse_id)+'.csv', index = True) 
        print('\nCSV String:\n', gfg_csv_data) 
        trainingForSVM(warehouse_id)
    return False

def trainingForSVM(whid):
    SVMController.polynomialSVM(whid)
    return False

def simulation():
    return False

def main():
    if os.path.exists('./hash.sqlite'):
        os.remove('./hash.sqlite')
    else:
        print("Can not delete the file as it doesn't exists")
    setupDB()
    createCSV()
    # simulation()
    

if __name__ == "__main__": main()