import os
import pandas as pd
import numpy as np

def read_file(input_file):
    with open(input_file) as f:
        num_rows, num_columns, num_drones, max_time, max_cargo = map(
            int, f.readline().split(" ")
        )

        # products
        num_products = int(f.readline())
        product_weights = list(map(int, f.readline().split(" ")))
        assert num_products == len(product_weights)
        products = [{"id": i, "weight": w} for i, w in enumerate(product_weights)]

        # # warehouses
        num_warehouses = int(f.readline())
        wh_list = []
        for i in range(num_warehouses):
            x, y = map(int, f.readline().split(" "))
            num_products_in_wh = list(map(int, f.readline().split(" ")))
            assert num_products == len(num_products_in_wh)
            wh_products = [{p["id"]: n} for p, n in zip(products, num_products_in_wh)]
            wh = {"id":i, "position":{"x":x,"y":y}, "products": wh_products}
            wh_list.append(wh)

        # order info
        order_list = []
        num_orders = int(f.readline())
        for i in range(num_orders):
            c = Counter()
            x, y = map(int, f.readline().split(" "))
            num_products_in_order = int(f.readline())
            order_products = list(map(int, f.readline().split(" ")))
            assert num_products_in_order == len(order_products)
            order_products = [products[x] for x in order_products]
            print(order_products)
            order = {
                "id":i, "position":{"x":x,"y":y}, "products": order_products, "isDelivered": False
            }
            order_list.append(order)
    return num_rows, num_columns, num_drones, max_time, max_cargo, products, wh_list, order_list

num_rows, num_columns, num_drones, max_time, max_cargo, products, wh_list, order_list = read_file('./busy_day.in')

print(wh_list[1]["products"][3])

