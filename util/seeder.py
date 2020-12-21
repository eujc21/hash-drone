import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ
from collections import Counter

def read_file(input_file):
    # This function reads the data input file and processes it
    # and example of the input file can be expressed in the report,
    # the presentation, or from the kaggle instruction and kaggle
    # project site for how the data is sent

    with open(input_file) as f: # Make the file into a data from and map the values
        num_rows, num_columns, num_drones, max_time, max_cargo = map(
            int, f.readline().split(" ")
        )

        # products (weights, ids, etc)
        num_products = int(f.readline())
        product_weights = list(map(int, f.readline().split(" ")))
        assert num_products == len(product_weights)
        products = [    # send to product model file to be organized and made into the sql database
            {"product_id": i, "product_weight": w} for i, w in enumerate(product_weights)
        ]

        # warehouses (locations, ids, products, etc)
        num_warehouses = int(f.readline())
        wh_list = []
        warehouse_products = []
        for i in range(num_warehouses): # For each warehouse in data input, process characteristics
            x, y = map(int, f.readline().split(" "))
            num_products_in_wh = list(map(int, f.readline().split(" ")))    # List of products in each warehouse
            assert num_products == len(num_products_in_wh)
            wh_products = [ # send to warehouse product model file to be organized and made into the sql database
                {   
                    "product_id":p["product_id"],
                    "qty": n,
                    "warehouse_id":i
                } for p, n in zip(products, num_products_in_wh)
            ]
            warehouse_products.append(wh_products)  # append the dictionaries and loop
            wh = {"warehouse_id":i, "dlx":x, "dly":y}   # send to warehouse model file for location and id value
            wh_list.append(wh)

        # order info (list of products, order id, etc)
        order_list = []
        order_product = []
        num_orders = int(f.readline())
        for i in range(num_orders): # For each order provided in the input file, process characteristics
            c = Counter()
            x, y = map(int, f.readline().split(" ")) # each order's location in the map
            num_products_in_order = int(f.readline())   # product qty
            order_products = list(map(int, f.readline().split(" ")))    # product ids
            assert num_products_in_order == len(order_products)
            order_products = [products[x] for x in order_products]
            counts = Counter(tok['product_id'] for tok in order_products)
            order = {   # send to order model file for location, order id, etc, to be made into sql database
                "id":i,
                "dlx":x,
                "dly":y,
                # "order_products":order_products,
                "isDelivered": False
            }
            order_product.append({"order_id":order["id"], "items":counts})  # send order products to model, also
            order_list.append(order)    # update order list dictionary, loop

    # return each dictionary to be placed into one database location
    return num_rows, num_columns, num_drones, max_time, max_cargo, products, wh_list, order_list, order_product, warehouse_products