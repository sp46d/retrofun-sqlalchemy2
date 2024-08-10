import csv
import os
from retrofun.db import Model, engine, Session
from retrofun.models import Product

products_path = os.path.join(os.path.dirname(__file__), 'data', 'products_with_id.csv')

def main():
    with Session() as session:
        with session.begin():
            Model.metadata.drop_all(engine)
            Model.metadata.create_all(engine)
            with open(products_path) as f:
                products = csv.DictReader(f)
                for row in products:
                    row['year'] = int(row['year'])
                    row['manufacturer_id'] = int(row['manufacturer_id'])
                    product = Product(**row)
                    session.add(product)
                    

if __name__ == '__main__':
    main()