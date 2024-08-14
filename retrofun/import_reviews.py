import os
import csv
from datetime import datetime
from sqlalchemy import select, delete
from retrofun.db import Session
from retrofun.models import Product, Customer, ProductReview


def main():
    reviews_path = os.path.join(os.path.dirname(__file__), 'data', 'reviews.csv')
    
    with Session() as session:
        with session.begin():
            session.execute(delete(ProductReview))
            
    with Session() as session:
        with session.begin():
            with open(reviews_path) as f:
                reader = csv.DictReader(f)
                
                all_customers: dict[str, Customer | None] = {}
                all_products: dict[str, Product | None] = {}
                
                for row in reader:
                    if row['product'] not in all_products:
                        p = session.scalar(select(Product).where(Product.name == row['product']))
                        all_products[row['product']] = p
                    
                    if row['customer'] not in all_customers:
                        c = session.scalar(select(Customer).where(Customer.name == row['customer']))
                        all_customers[row['customer']] = c
                    
                    pr = ProductReview(timestamp=datetime.strptime(row['timestamp'],
                                                                   "%Y-%m-%d %H:%M:%S"),
                                       rating=int(row['rating']),
                                       comment=row['comment'] or None,
                                       product=all_products[row['product']],
                                       customer=all_customers[row['customer']])
                    session.add(pr)
                    

if __name__ == '__main__':
    main()