import csv
import os
from retrofun.db import Model, engine, Session
from retrofun.models import Product, Manufacturer, Country

products_path = os.path.join(os.path.dirname(__file__), 'data', 'products.csv')


def main():
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

    with Session() as session:
        with session.begin():
            with open(products_path) as f:
                reader = csv.DictReader(f)
                all_manufacturers: dict[str, Manufacturer] = {}
                all_countries: dict[str, Country] = {}
                
                for row in reader:
                    row['year'] = int(row['year'])
                    manufacturer = row.pop('manufacturer')
                    countries = row.pop('country').split('/')
                    p = Product(**row)
                    
                    if manufacturer not in all_manufacturers:
                        m = Manufacturer(name=manufacturer)
                        session.add(m)
                        all_manufacturers[manufacturer] = m
                    all_manufacturers[manufacturer].products.append(p)
                    
                    for country in countries:
                        if country not in all_countries:
                            c = Country(name=country)
                            session.add(c)
                            all_countries[country] = c
                        all_countries[country].products.append(p)

if __name__ == '__main__':
    main()