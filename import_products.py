import csv
from db import Model, engine, Session
from models import Product


def main():
    with Session() as session:
        with session.begin():
            Model.metadata.drop_all(engine)
            Model.metadata.create_all(engine)
            with open('products.csv') as f:
                products = csv.DictReader(f)
                for row in products:
                    row['year'] = int(row['year'])
                    product = Product(**row)
                    session.add(product)
                    

if __name__ == '__main__':
    main()