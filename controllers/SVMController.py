from database import hash_database
from models import OrderModel, ProductModel, OrderProductModel, WarehouseProductModel
from controllers import WarehouseProductController, WarehouseController
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from sqlalchemy.sql import label

# Data Science Functionality
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from thundersvm import SVC
import pickle

# Helper Functions
from functools import reduce
from util import distance
from util.isOrderOptimized import _is_order_optimized_
import time

# Sklearn libraries
from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score

def getSVMTable(warehouse_id):
    # This function creates the svm tables necessary for the subsequent function beneath to process, classify
    # and model the results

    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)     # Start a sqlite session to pull values from the data base
    session = Session()
    svmtable = []
    warehouse_location = WarehouseController.getWHLocation(warehouse_id)    # get warehouse location information
    print(warehouse_location)
    distinct_ids = session.query(OrderModel.id).distinct()  # Get distinct order ids, each 1250
    for op in distinct_ids:     # op=order product relationship. collection from distinc ids
        obj = {}
        obj["order_id"] = op[0] # Associate each order id's to their products
        for order_id in op:     # From op, get the order id ONLY
            # Create dictionaries for each order's location values, product availability against each warehouse,
            # weight of the order, etc for SVM features and SVM calculations
            order = session.query(OrderModel).filter(OrderModel.id == order_id).first()
            obj["order_location_x"] = order.dlx
            obj["order_location_y"] = order.dly
            # Retrieve the Order ID's associated model
            order_results = session.query(OrderProductModel).filter(OrderProductModel.order_id == order_id).all()
            # order_results = session.query(OrderProductModel).all()
            obj["has_all_available_products"] = []
            obj["percentage_availability_of_products"] = []
            obj["total_weight_of_order"] = []
            for result in order_results:    # Can use the model to get the qty of products per order
                qty = result.getQty()
                # Get product from data base
                product = session.query(ProductModel).filter(ProductModel.product_id == result.product_id).first()
                total_weight_of_product = qty*product.product_weight    # combine product weights with product qty
                # Get warehouse quantities from database
                wh_qty = WarehouseProductController.getWareHouseProductQty(warehouse_id, result.product_id)
                # obj["inventory_product_"+str(result.product_id)+"_qty"] = wh_qty
                # obj["product_"+str(result.product_id)+"_qty"] = qty
                obj["total_weight_of_order"].append(total_weight_of_product)    # Appending dictionary of new weight
                obj["has_all_available_products"].append(True if qty == wh_qty else False)  # Appending dictionary bool
                # Get percentage of products available to the order from the warehouse
                obj["percentage_availability_of_products"].append((qty/wh_qty) if qty <= wh_qty else 0)

            # Final calculation weight of order products to warehouse products
            obj["percentage_availability_of_products"] = reduce(
                lambda a, b: a + b, obj["percentage_availability_of_products"]
            ) / len(obj["percentage_availability_of_products"])

            # Final check over if the warehouse can cover the order id
            obj["has_all_available_products"] = 1 if all(obj["has_all_available_products"]) == True else 0
            obj["warehouse_location_x"] = warehouse_location["wh_location_x"]
            obj["warehouse_location_y"] = warehouse_location["wh_location_y"]
            obj["total_weight_of_order"] = reduce(
                lambda a, b: a + b, obj["total_weight_of_order"]
            )
            obj["distance_order_from_warehouse"] = distance(      # Mark the distance classifier with a 1 or a 0 (Test)
                {
                    0: obj["warehouse_location_x"],
                    1: obj["warehouse_location_y"]
                },
                {
                    0: obj["order_location_x"],
                    1: obj["order_location_y"]
                }
             )
            obj["classifier"] = 1 if (      # Test classifier (actual classifier under utility file
                obj["distance_order_from_warehouse"] < 300 and obj["percentage_availability_of_products"] > 0.40
            ) else -1
            #     obj["distance_order_from_warehouse"] <  300 and (obj["percentage_availability_of_products"] < 0.60 or obj["percentage_availability_of_products"] > 0.30) and  obj["total_weight_of_order"] < 200
            # ) else 0
        svmtable.append(obj) # Append table with SVM values (classifier, values ready to be modeled)
    return svmtable

def polynomialSVM(whid):
    # This function models the SVM of orders in relation (the features) to each warehouse based on the percentage
    # of products the warehouse of focus can supply and the distance to warehouse of focus

    # Retrieve Dataset
    dataset = _is_order_optimized_(
        './assets/warehouse_'+str(whid)+'.csv',
    )
    X = dataset.drop('classifier',axis=1)
    Y = dataset["classifier"]

    # Splitting data into train and test
    xTrain, xTest, yTrain, yTest = train_test_split(
        X,
        Y,
        test_size = 0.20,
        random_state=0
    )

    # Feature scaling
    sc = StandardScaler()
    xTrain = sc.fit_transform(xTrain)
    xTest = sc.fit_transform(xTest)

    # Fitting Kernel SVM to the Training set.
    svcClassifier = SVC(
        kernel='rbf',
        random_state=0,
        max_mem_size=50000,
        n_jobs=8,
        C=100   # This value can vary for whether the margin is too 'hard' or too 'soft'
    )

    # pickling the files (serializing them and storing them)
    # This way, the model can run the data against other data
    svcClassifier.fit(xTrain,yTrain)
    svc_pickle = './assets/sv_pickle_rbf_'+str(whid)+'.sav'
    pickle.dump(svcClassifier, open(svc_pickle, 'wb'))

    # Predicting the test results
    polyPred = svcClassifier.predict(xTest)
    print(polyPred)

    # Confusion Matrix Print: SVM Classifier polyTest against the Test Labeled Data yTest
    print("Confusion Matrix")
    print(confusion_matrix(yTest, polyPred))
    print("\n")
    
    # Classification report
    print("Classification Report")
    print(classification_report(yTest, polyPred))
    print("\n")

    # Applying k-fold cross validation for accuracy purposes
    accuracies = cross_val_score(estimator = svcClassifier, X=xTrain, y=yTrain, cv=10)
    print(accuracies.mean())
    print(accuracies.std())

    # Visualising the Test set results
    from matplotlib.colors import ListedColormap
    X_set, y_set = xTest, yTest
    X1, X2 = np.meshgrid(
        np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
        np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01)
    )
    plt.contourf(       # Creating the contouring lines
        X1,
        X2,
        svcClassifier.\
            predict(np.array([X1.ravel(), X2.ravel()]).T).\
                reshape(X1.shape),
        alpha = 0.5,
        cmap = ListedColormap(('blue', 'black'))
    )
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    for i, j in enumerate(np.unique(y_set)):    # Creating the scatter plots
        plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                    c = ListedColormap(('red', 'green'))(i), label = j)

    # labeling each plot
    plt.title('Kernel SVM (Training Data) Warehouse: ' + str(whid))
    plt.xlabel('Distance From Warehouse')
    plt.ylabel('Percentage of Available Products')
    plt.legend()
    plt.savefig('./assets/RBF'+str(whid)+'_'+str(int(time.time()))+'.png')    
    plt.close()
    return False