### Hash Code Delivery

### Setup Project
```bash
python -m venv code-base
source code-base-bin/activate
pip install -r requirements.txt

install this file script (needs to be built):
https://github.com/Xtra-Computing/thundersvm/blob/d38af58e0ceb7e5d948f3ef7d2c241ba50133ee6/python/dist/thundersvm-cu10-0.2.0-py3-none-win_amd64.whl
Thunder SVM


python main.py
```

```bash
.
├── accuracy.txt
├── assets
│   ├── busy_day.in
│   ├── hashcode_delivery_instructions.pdf
│   ├── Hash-Code-Drone-Delivery.minder
│   ├── hashcode-drone-delivery.zip
│   ├── Polynomial_0_1608501928.png
│   ├── Polynomial_1_1608501949.png
│   ├── Polynomial_2_1608501970.png
│   ├── Polynomial_3_1608501991.png
│   ├── Polynomial_4_1608502012.png
│   ├── Polynomial_5_1608502034.png
│   ├── Polynomial_6_1608502057.png
│   ├── Polynomial_7_1608502078.png
│   ├── Polynomial_8_1608502101.png
│   ├── Polynomial_9_1608502123.png
│   ├── sv_pickle_0.sav
│   ├── sv_pickle_1.sav
│   ├── sv_pickle_2.sav
│   ├── sv_pickle_3.sav
│   ├── sv_pickle_4.sav
│   ├── sv_pickle_5.sav
│   ├── sv_pickle_6.sav
│   ├── sv_pickle_7.sav
│   ├── sv_pickle_8.sav
│   ├── sv_pickle_9.sav
│   ├── warehouse_0.csv
│   ├── warehouse_1.csv
│   ├── warehouse_2.csv
│   ├── warehouse_3.csv
│   ├── warehouse_4.csv
│   ├── warehouse_5.csv
│   ├── warehouse_6.csv
│   ├── warehouse_7.csv
│   ├── warehouse_8.csv
│   └── warehouse_9.csv
├── controllers
│   ├── OrderController.py
│   ├── SVMController.py
│   ├── WarehouseController.py
│   └── WarehouseProductController.py
├── database
│   ├── hash_database.py
│   ├── __init__.py
├── hash.sqlite
├── main.py
├── models
│   ├── __init__.py
│   ├── order_model.py
│   ├── order_product_model.py
│   ├── product_model.py
│   ├── svm_model.py
│   ├── warehouse_model.py
│   └── warehouse_product_model.py
├── README.md
├── requirements.txt
├── thundersvm
│   ├── __init__.py
│   ├── libthundersvm.so
│   └── thundersvm.py
├── tree.md
└── util
    ├── distance.py
    ├── __init__.py
    ├── isOrderOptimized.py
    └── seeder.py

11 directories, 78 files
```
[Pre Processing](https://www.kaggle.com/srii96/hashcode-problem-understanding-pre-process)

[Greedy Solution](https://www.kaggle.com/egrehbbt/greedy-solution-post-processing)

[Beginners Guide to SQLALchemy In Python For Database Operations](https://analyticsindiamag.com/beginners-guide-to-sqlalchemy-in-python-for-database-operations/)

[An Introduction To Venv](http://cewing.github.io/training.python_web/html/presentations/venv_intro.html)

[Seeders](https://sqlalchemy-seeder.readthedocs.io/en/latest/usage.html)

[SQLite Database Browser](http://blog.sudobits.com/2012/03/11/sqlite-database-browser-for-ubuntu/)

[SQLAlchemy Core - Creating Table](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_creating_table.htm)

[Session Basics](https://docs.sqlalchemy.org/en/14/orm/session_basics.html)

[How to Use Python SQLite3 Using SQLAlchemy](https://medium.com/level-up-programming/how-to-use-python-sqlite3-using-sqlalchemy-158f9c54eb32)

[Python SQLite3 tutorial #droptable](https://likegeeks.com/python-sqlite3-tutorial/#Drop-table)

[Creating a Connection to a SQLite Database](https://www.digitalocean.com/community/tutorials/how-to-use-the-sqlite3-module-in-python-3#step-1-%E2%80%94-creating-a-connection-to-a-sqlite-database)

[Using Flask With Python, SQLite, and SQLAlchemy](https://realpython.com/python-sqlite-sqlalchemy/#using-flask-with-python-sqlite-and-sqlalchemy)

[Intro to Python Database Management with SQLAlchemy](https://hackersandslackers.com/python-database-management-sqlalchemy)

[Design Patterns - MVC Pattern](https://www.tutorialspoint.com/design_pattern/mvc_pattern.htm)

[Thunder SVM](https://github.com/Xtra-Computing/thundersvm)

[Thunder SVM Script](https://github.com/Xtra-Computing/thundersvm/tree/d38af58e0ceb7e5d948f3ef7d2c241ba50133ee6)

[Thunder SVM Script for Windows](https://github.com/Xtra-Computing/thundersvm/blob/d38af58e0ceb7e5d948f3ef7d2c241ba50133ee6/python/dist/thundersvm-cu10-0.2.0-py3-none-win_amd64.whl)