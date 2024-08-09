import csv
import os
from retrofun.db import Model, engine, Session
from retrofun.models import Product

data_path = os.path.join(os.path.dirname(__file__), 'data', 'products.csv')

def main():
    with Session() as session:
        with session.begin():
            Model.metadata.drop_all(engine)
            Model.metadata.create_all(engine)
            with open(data_path) as f:
                products = csv.DictReader(f)
                for row in products:
                    row['year'] = int(row['year'])
                    product = Product(**row)
                    session.add(product)
                    

if __name__ == '__main__':
    main()