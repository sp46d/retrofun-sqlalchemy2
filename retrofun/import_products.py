import csv
import os
from retrofun.db import Model, engine, Session
from retrofun.models import Product, Manufacturer

products_path = os.path.join(os.path.dirname(__file__), 'data', 'products.csv')


def main():
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            with open(products_path) as f:
                reader = csv.DictReader(f)
                all_manufacturers = {}
                
                for row in reader:
                    row['year'] = int(row['year'])
                    manufacturer = row.pop('manufacturer')
                    p = Product(**row)
                    
                    if manufacturer not in all_manufacturers:
                        m = Manufacturer(name=manufacturer)
                        session.add(m)
                        all_manufacturers[manufacturer] = m
                    all_manufacturers[manufacturer].products.append(p)
                    

if __name__ == '__main__':
    main()