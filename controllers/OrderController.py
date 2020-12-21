from database import hash_database
from models import order_model
from sqlalchemy.orm import sessionmaker

# This function creates a SQLite database session to pull the order id's
# for when desired

def getOrders():
    dbms = hash_database.HashDatabse(hash_database.SQLITE, dbname='hash.sqlite')
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    for instance in session.query(order_model.OrderModel).order_by(order_model.OrderModel.id):
        print(instance.getId())
    return False
