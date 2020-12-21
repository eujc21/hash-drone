from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Table,MetaData, Column, Integer, String, Text, DateTime, Float, Boolean, PickleType, ForeignKey
from models import product_model, order_model, warehouse_model

# Namespaces
SQLITE = 'sqlite'

# Table Names
PRODUCTS = 'products'
ORDERS = 'orders'
ORDERPRODUCTS = 'order_products'
WAREHOUSES = 'warehouses'
WAREHOUSEPRODUCTS = 'warehouse_products'



class HashDataBase:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None
    # Data base engine create
    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys(): # Calling the engine if connection is good
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
        else:
            print("DBType is not found in DB_ENGINE")

    # Create a base table for the database to alter and append
    def create_db_tables(self):
        metadata = MetaData()
        products = Table(   # Main columns for products (weight, id, product type)
            PRODUCTS, metadata,
            Column('id', Integer, primary_key=True, nullable=False),
            Column('product_id', Integer, nullable=False),
            Column('product_weight', Float, nullable=False)
        )
        orders = Table(     # Main columns for orders (bool for delivered, id, x and y coords)
            ORDERS, metadata,
            Column('id', Integer, primary_key=True, nullable=False),
            Column('dlx', Integer, nullable=False),
            Column('dly', Integer, nullable=False),
            Column('isDelivered', Boolean, nullable=False)
        )
        order_product = Table(  # Main columns for the products of orders (id, qty, order id, product type)
            ORDERPRODUCTS, metadata,
            Column('id', Integer, primary_key=True, nullable=False),
            Column('product_id', Integer, ForeignKey(product_model.ProductModel.product_id), nullable=False),
            Column('order_id', Integer, ForeignKey(order_model.OrderModel.id), nullable=False),
            Column('qty', Integer, nullable=False)
        )
        warehouses = Table(     # Main columns for warehouses (id, warehouse number, x and y coords)
            WAREHOUSES, metadata,
            Column('id', Integer, primary_key=True, nullable=False),
            Column('warehouse_id', Integer, ForeignKey(product_model.ProductModel.product_id), nullable=False),
            Column('dlx', Integer, nullable=False),
            Column('dly', Integer, nullable=False)
        )
        warehouse_products = Table( # Main columns for products of warehouses (id, product type, warehouse id, qty)
            WAREHOUSEPRODUCTS, metadata,
            Column('id', Integer, primary_key=True, nullable=False),
            Column('product_id', Integer, ForeignKey(product_model.ProductModel.product_id), nullable=False),
            Column('warehouse_id', Integer, ForeignKey(warehouse_model.WarehouseModel.warehouse_id), nullable=False),
            Column('qty', Integer, nullable=False)
        )
        try:    # debug for creating the table
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occured during Table creation!")
            print(e)



    def execute_query(self, query=''):
        # this function is the basis for starting a query with the hashtable
        # this function connects to the engine to start up the database
        if query == '': return
        print(query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        # This function prints all data from the database for necessary debugging and when necessary to view
        # all data present in the table
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        print(query)
        with self.db_engine.connect() as connection:    # Connect with the hashtable enginer
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:  # if good to go, print each row and close when finished
                    print(row)
                result.close()
        print("\n")
