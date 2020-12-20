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
    dbms = hash_database.HashDataBase(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    svmtable = []
    warehouse_location = WarehouseController.getWHLocation(warehouse_id)
    print(warehouse_location)
    distinct_ids = session.query(OrderModel.id).distinct()
    for op in distinct_ids:
        obj = {}
        obj["order_id"] = op[0]
        for order_id in op:
            order = session.query(OrderModel).filter(OrderModel.id == order_id).first()
            obj["order_location_x"] = order.dlx
            obj["order_location_y"] = order.dly
            order_results = session.query(OrderProductModel).filter(OrderProductModel.order_id == order_id).all()
            # order_results = session.query(OrderProductModel).all()
            obj["has_all_available_products"] = []
            obj["percentage_availability_of_products"] = []
            obj["total_weight_of_order"] = []
            for result in order_results:
                qty = result.getQty()
                product = session.query(ProductModel).filter(ProductModel.product_id == result.product_id).first()
                total_weight_of_product = qty*product.product_weight
                wh_qty = WarehouseProductController.getWareHouseProductQty(warehouse_id, result.product_id)
                # obj["inventory_product_"+str(result.product_id)+"_qty"] = wh_qty
                # obj["product_"+str(result.product_id)+"_qty"] = qty
                obj["total_weight_of_order"].append(total_weight_of_product)
                obj["has_all_available_products"].append(True if qty == wh_qty else False)
                obj["percentage_availability_of_products"].append((qty/wh_qty) if qty <= wh_qty else 0)
            obj["percentage_availability_of_products"] = reduce(
                lambda a, b: a + b, obj["percentage_availability_of_products"]
            ) / len(obj["percentage_availability_of_products"])
            obj["has_all_available_products"] = 1 if all(obj["has_all_available_products"]) == True else 0
            obj["warehouse_location_x"] = warehouse_location["wh_location_x"]
            obj["warehouse_location_y"] = warehouse_location["wh_location_y"]
            obj["total_weight_of_order"] = reduce(
                lambda a, b: a + b, obj["total_weight_of_order"]
            )
            obj["distance_order_from_warehouse"] = distance(
                {
                    0: obj["warehouse_location_x"],
                    1: obj["warehouse_location_y"]
                },
                {
                    0: obj["order_location_x"],
                    1: obj["order_location_y"]
                }
             )
            obj["classifier"] = 1 if (
                obj["distance_order_from_warehouse"] < 300 and obj["percentage_availability_of_products"] > 0.40
            ) else -1
            #     obj["distance_order_from_warehouse"] <  300 and (obj["percentage_availability_of_products"] < 0.60 or obj["percentage_availability_of_products"] > 0.30) and  obj["total_weight_of_order"] < 200
            # ) else 0
        svmtable.append(obj)
    return svmtable

def polynomialSVM(whid):
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
        kernel='polynomial',
        random_state=0,
        max_mem_size=50000,
        n_jobs=4,
        C=0.5
    )
    svcClassifier.fit(xTrain,yTrain)
    svc_pickle = './assets/sv_pickle_'+str(whid)+'.sav'
    pickle.dump(svcClassifier, open(svc_pickle, 'wb'))
    # Predicting the test results
    polyPred = svcClassifier.predict(xTest)
    print(polyPred)
    # Confusion Matrix
    print("Confusion Matrix")
    print(confusion_matrix(yTest, polyPred))
    print("\n")
    
    # Classification report
    print("Classification Report")
    print(classification_report(yTest, polyPred))
    print("\n")

    # Applyinbg k-fold cross validation
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
    plt.contourf(
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
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                    c = ListedColormap(('red', 'green'))(i), label = j)
    plt.title('Kernel SVM (Training Data) Warehouse: ' + str(whid))
    plt.xlabel('Distance From Warehouse')
    plt.ylabel('Percentage of Available Products')
    plt.legend()
    plt.savefig('./assets/Polynomial_'+str(whid)+'_'+str(int(time.time()))+'.png')    
    plt.close()
    return False