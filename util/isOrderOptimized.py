import pandas as pd
def _is_order_optimized_ (in_file):
    # The goal of this function is to classify orders relative to each warehouse
    # each warehouse of focus has its own classification 'box plot' and the features the
    # classifier is based off of is the percentage of products available of the orders
    # for the relative warehouse of focus and the distance the orders are relative
    # to the warehouse of focus
    file = pd.read_csv( # Pull columns that will be used
        in_file,
        usecols = [
            'distance_order_from_warehouse',
            'percentage_availability_of_products',
        ]
    )
    pap_class = file['percentage_availability_of_products'].mean()  # Get the mean of the column as a bar to set
    dist_class = file['distance_order_from_warehouse'].mean()   # Ge the mean of the column as a bar to set

    ord_classified = [] # Create a new dictionary for the classified order markers to go into
    for index, row in file.iterrows():  # go through each row of the input file and classify
        if (row['percentage_availability_of_products'] > pap_class) & \
                (row['distance_order_from_warehouse'] < dist_class):
            ord_classified.append(1)
        else:
            ord_classified.append(-1)

    file['classifier'] = ord_classified # append dataframe with classified markers
    return file
