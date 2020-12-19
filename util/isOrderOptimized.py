import pandas as pd

# The goal of this function is to classify orders relative to each
# warehouse that is present on the map based on the distance and
# the availability of the products to each order

def _is_order_optimized_ (in_file):
    file = pd.read_csv(in_file)
    pap_class = file['percentage_availability_of_products'].mean()
    dist_class = file['distance_order_from_warehouse'].mean()

    ord_classified = []
    for index, row in file.iterrows():
        if (row['percentage_availability_of_products'] > pap_class) & \
                (row['distance_order_from_warehouse'] < dist_class):
            ord_classified.append(1)
        else:
            ord_classified.append(-1)

    file['classifier'] = ord_classified
    return file
