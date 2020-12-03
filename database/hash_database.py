from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Table,MetaData, Column, Integer, String, Text, DateTime, Float, Boolean, PickleType

SQLITE = 'sqlite'

# Table Names
PRODUCTS = 'products'


class HashDatabse:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None
    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        products = Table(
            PRODUCTS, metadata,
            Column('id', Integer, primary_key=True, nullable=False),
            Column('product_id', Integer, nullable=False),
            Column('product_weight', Float, nullable=False)
        )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occured during Table creation!")
            print(e)

    def execute_query(self, query=''):
        if query == '': return
        print(query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)
                result.close()
        print("\n")
