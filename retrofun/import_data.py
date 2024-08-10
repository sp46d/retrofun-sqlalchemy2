import csv
import os
from retrofun.db import Model, engine, Session
from retrofun.models import Product, Manufacturer


products_path = os.path.join(os.path.dirname(__file__), 'data', 'products_with_id.csv')
manufacturers_path = os.path.join(os.path.dirname(__file__), 'data', 'manufacturers.csv')

def main():
    with Session() as session:
        with session.begin():
            Model.metadata.drop_all(engine)
            Model.metadata.create_all(engine)
            # Load products_with_id.csv and add it to database
            with open(products_path) as f:
                products = csv.DictReader(f)
                for row in products:
                    row['year'] = int(row['year'])
                    row['manufacturer_id'] = int(row['manufacturer_id'])
                    product = Product(**row)
                    session.add(product)
            # Load manufacturer.csv and add it to database
            with open(manufacturers_path) as f:
                manufacturers = csv.DictReader(f)
                for row in manufacturers:
                    manufacturer = Manufacturer(**row)
                    session.add(manufacturer)
                    

if __name__ == '__main__':
    main()