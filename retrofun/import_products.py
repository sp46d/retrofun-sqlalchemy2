import csv
import os
from sqlalchemy import delete
from retrofun.db import Session
from retrofun.models import Product, Manufacturer, Country, ProductCountry

products_path = os.path.join(os.path.dirname(__file__), 'data', 'products.csv')


def main():
    with Session() as session:
        with session.begin():
            session.execute(delete(ProductCountry))
            session.execute(delete(Product))
            session.execute(delete(Manufacturer))
            session.execute(delete(Country))

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