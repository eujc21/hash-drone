import os
from database import hash_database
from models import ProductModel, OrderModel,OrderProductModel, WarehouseModel, WarehouseProductModel
from controllers import OrderController, SVMController, WarehouseController, WarehouseProductController
from sqlalchemy.orm import sessionmaker
from util.seeder import read_file
import pandas as pd

def setupDB():
    # This function sets up the database. After processing the input file function and getting each dictionary
    # the dataframes need to be put into the SQL database for the information to be used later and throughout
    # each simulation

    num_rows, num_columns, num_drones, max_time, max_cargo, products, wh_list, order_list, order_product, warehouse_products = read_file('./assets/busy_day.in')
    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')   # Creating database session to call on
    dbms.create_db_tables()
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()

    # add each product, order, order products, warehouse, and warehouse products to database
    for product in products:
        session.add(ProductModel(**product))    # append database with product types
    for order in order_list:
        session.add(OrderModel(**order))    # append database with order ids
    for order in order_product:
        # session.add(order_product_model.OrderModel(**order))
        order_id = order["order_id"]
        for key in dict(order["items"]).keys():     # for each product of the orders, add with an id, qty, weight, etc
            order["items"][key]
            session.add(
                OrderProductModel(      # order product model file arguments
                    **{
                        "order_id":order_id,
                        "product_id": key,
                        "qty": order["items"][key]
                    }
                )
            )
    for warehouse in wh_list:
        session.add(WarehouseModel(**warehouse))    # append database with warehouse ids

    for wh_product in warehouse_products:   # append database with warehouse product ids and quantities
        for wh_pr in wh_product:
            session.add(WarehouseProductModel(**wh_pr))
    session.commit()

    
def createCSV():
    # This function is the set up for the SVM model for determining the best orders for each drone
    # to process first. A number of features and factors work into this but each SVM processes is
    # relative to each warehouse present

    warehouses = WarehouseController.getWarehouses()    # Get warehouse list to train on
    # warehouse_id= input("Which warehouse would you like to train on , pick 0-9: ")

    # for warehouse_id in warehouses:
    for warehouse_id in warehouses:
        svmTable = SVMController.getSVMTable(warehouse_id)  # From controller, get svm table function from warehouse
        # This function call is very important to which a lot of variables are considered and makes the table

        group_value = []
        for value in svmTable:  # for each value generated from svm table, append groun value
            group_value.append(value)
        df = pd.DataFrame(group_value)  # data frame the dictionary
        df.fillna(0, inplace=True)  # fill
        gfg_csv_data = df.to_csv('./assets/warehouse_'+str(warehouse_id)+'.csv', index = True)  # create a file
        print('\nCSV String:\n', gfg_csv_data) 
        trainingForSVM(warehouse_id)    # This function calls for training the svm table values per each warehouse
    return False

def trainingForSVM(whid):
    # This function calls the training for each warehouse for the SVM
    # this function calls the svm controller file to do a polynomial kernel
    SVMController.polynomialSVM(whid)
    return False

def simulation():
    # This function runs the simulation
    # This function is currently not implemented
    return False

def main():
    # Call each function the start and create a path for the hashtable
    if os.path.exists('./hash.sqlite'):
        os.remove('./hash.sqlite')
    else:
        print("Can not delete the file as it doesn't exists")
    setupDB()
    createCSV()
    # simulation()
    

if __name__ == "__main__": main()