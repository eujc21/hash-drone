import os
import pandas as pd
import numpy as np

# The goal of this function is to take the order distance,
# order product, warehouse product, and drone weight
# and determine if the order is optimized for that warehouse

def _is_order_optimized_ (ord_dist, ord_x, ord_y, wh_x, wh_y,  wh_prod, ord_prod, drone_weight )

    # Lets begin with creating a distance threshold parameter for the order.
    # Just as a percentage or a HPF, using the order's own coords
    # compared to the warehouse's can help gauge what a good distance
    # from the order to the warehouse would be. High Distances need to be filtered
    # as not an optimized order

    learn_fact = 1.5 # Can adjust this for determining a good threshold filter

    dist_use = abs(wh_x-ord_x) if (abs(wh_x-ord_x) >= abs(wh_y-ord_y)) else abs(wh_y-ord_y)
    dist_check = 1 if (ord_dist < dist_use * learn_fact) else 0

    if dist_check == 1:

    else:
        dev_op == 0;


    return dev_op
