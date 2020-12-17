import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ
from collections import Counter

def read_file(input_file):
    with open(input_file) as f:
        num_rows, num_columns, num_drones, max_time, max_cargo = map(
            int, f.readline().split(" ")
        )

        # products
        num_products = int(f.readline())
        product_weights = list(map(int, f.readline().split(" ")))
        assert num_products == len(product_weights)
        products = [
            {"product_id": i, "product_weight": w} for i, w in enumerate(product_weights)
        ]

        # warehouses
        num_warehouses = int(f.readline())
        wh_list = []
        warehouse_products = []
        for i in range(num_warehouses):
            x, y = map(int, f.readline().split(" "))
            num_products_in_wh = list(map(int, f.readline().split(" ")))
            assert num_products == len(num_products_in_wh)
            wh_products = [
                {   
                    "product_id":p["product_id"],
                    "qty": n,
                    "warehouse_id":i
                } for p, n in zip(products, num_products_in_wh)
            ]
            warehouse_products.append(wh_products)
            wh = {"warehouse_id":i, "dlx":x, "dly":y}
            wh_list.append(wh)
        # order info
        order_list = []
        order_product = []
        num_orders = int(f.readline())
        for i in range(num_orders):
            c = Counter()
            x, y = map(int, f.readline().split(" "))
            num_products_in_order = int(f.readline())
            order_products = list(map(int, f.readline().split(" ")))
            assert num_products_in_order == len(order_products)
            order_products = [products[x] for x in order_products]
            counts = Counter(tok['product_id'] for tok in order_products)
            order = {
                "id":i,
                "dlx":x,
                "dly":y,
                # "order_products":order_products,
                "isDelivered": False
            }
            order_product.append({"order_id":order["id"], "items":counts})
            order_list.append(order)
    return num_rows, num_columns, num_drones, max_time, max_cargo, products, wh_list, order_list, order_product, warehouse_products