from database import hash_database
from models import product_model
from sqlalchemy.orm import sessionmaker

def main():
    dbms = hash_database.HashDatabse(hash_database.SQLITE, dbname='hash.sqlite')
    dbms.create_db_tables()
    Session = sessionmaker(bind=dbms.db_engine)
    session = Session()
    print(session)
    new_product = product_model.ProductModel(
        product_id='1',
        product_weight=23
    )
    session.add(new_product)
    session.commit()
    dbms.print_all_data(hash_database.PRODUCTS)

if __name__ == "__main__": main()