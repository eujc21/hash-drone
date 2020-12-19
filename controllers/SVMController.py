from database import hash_database
from models import OrderModel, ProductModel, OrderProductModel, WarehouseProductModel
from controllers import WarehouseProductController, WarehouseController
from util import distance
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from sqlalchemy.sql import label
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import datasets
from functools import reduce
import numpy as np

def make_meshgrid(x, y, z, h=.02):
    x_min, x_max  = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1 ,y.max() + 1
    z_min, z_max = z.min() - 1 ,z.max() + 1
    xx, yy, zz = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h), np.arange(z_min, z_max))
    return xx, yy, zz

def plot_contours(ax, clf, xx, yy, zz, **params):
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel(), zz.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, zz, Z, **params)
    return out  

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
                obj["distance_order_from_warehouse"] < 300 and obj["percentage_availability_of_products"] > 0.60 and  obj["total_weight_of_order"] < 200
            ) else 2 if (
                obj["distance_order_from_warehouse"] <  300 and (obj["percentage_availability_of_products"] < 0.60 or obj["percentage_availability_of_products"] > 0.30) and  obj["total_weight_of_order"] < 200
            ) else 0
        svmtable.append(obj)
    return svmtable

def polynomialSVM():
    dataset = pd.read_csv(
        './assets/warehouse_1.csv',
        usecols = [
            'distance_order_from_warehouse',
            'percentage_availability_of_products',
            'total_weight_of_order',
            'classifier'
        ]
    )
    X = dataset.drop('classifier',axis=1)
    Y = dataset["classifier"]
    # X = X[np.logical_or(Y==0,Y==1)]
    # Y = Y[np.logical_or(Y==0,Y==1)]
    # print(datasets.load_iris().target)
    xTrain, xTest, yTrain, yTest = train_test_split(
        X,
        Y,
        test_size = 0.20,
        random_state=0
    )
    svcClassifier = SVC(kernel='poly', C=0.1)
    svcClassifier.fit(xTrain,yTrain)
    polyPred = svcClassifier.predict(xTest)
    print("Confusion Matrix")
    print(confusion_matrix(yTest, polyPred))
    print("\n")
    print("Classification Report")
    print(classification_report(yTest, polyPred))
    print("\n")
    # z = lambda x,y: (-svcClassifier.intercept_[0]-svcClassifier.coef_[0][0]*x -svcClassifier.coef_[0][1]*y) / svcClassifier.coef_[0][2]
    # tmp = np.linspace(-5,5,30)
    # x,y = np.meshgrid(tmp,tmp)
    # fig, ax = plt.subplots()# title for the plots
    # title = "Decision surface of linear SVC "
    # # Set-up grid for plotting.
    # xFeatureNames = list(X)
    # yFeatureNames = list(set(Y))
    # X0, X1, X2= X["percentage_availability_of_products"], X["distance_order_from_warehouse"], X["total_weight_of_order"]
    # xx, yy, zz = make_meshgrid(X0, X1, X2)
    # plot_contours(ax, svcClassifier.fit(X,Y), xx, yy, zz, cmap=plt.cm.coolwarm, alpha=0.8)
    # ax.scatter(X0, X1, c=yFeatureNames, cmap=plt.cm.coolwarm, s=20, edgecolors="k")
    # ax.set_ylabel("{}".format(xFeatureNames))
    # ax.set_xlabel("{}".format(yFeatureNames))
    # ax.set_xticks(())
    # ax.set_yticks(())
    # ax.set_title(title)
    # plt.show()
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot3D(X[Y==0,0], X[Y==0,1], X[Y==0,2],'ob')
    # ax.plot3D(X[Y==1,0], X[Y==1,1], X[Y==1,2],'sr')
    # ax.plot_surface(x, y, z(x,y))
    # ax.view_init(30, 60)
    # plt.show()
    return False