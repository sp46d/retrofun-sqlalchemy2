import os
import csv
from sqlalchemy import select, delete
from retrofun.db import Session
from retrofun.models import Product, Customer, Order, OrderItem
from datetime import datetime


def main():
    orders_path = os.path.join(os.path.dirname(__file__), 'data', 'orders.csv')
    
    with Session() as session:
        with session.begin():
            session.execute(delete(Customer))
            session.execute(delete(Order))
            session.execute(delete(OrderItem))

    with Session() as session:
        with session.begin():
            with open(orders_path) as f:
                reader = csv.DictReader(f)
                all_customers: dict[str, Customer] = {}
                all_products: dict[str, Product | None] = {}
                
                for row in reader:
                    if row['name'] not in all_customers:
                        c = Customer(name=row['name'],
                                     address=row['address'],
                                     phone=row['phone'])
                        all_customers[row['name']] = c
                    o = Order(timestamp=datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S"))
                    all_customers[row['name']].orders.add(o)
                    session.add(o)

                    p = all_products.get(row['product1'])
                    if p is None:
                        p = session.scalar(select(Product).where(Product.name == row['product1']))
                        all_products[row['product1']] = p
                    o.order_items.append(OrderItem(
                        unit_price=float(row['unit_price1']),
                        quantity=int(row['quantity1']),
                        product=p))
                    
                    if row['product2']:
                        p = all_products.get(row['product2'])
                        if p is None:
                            p = session.scalar(select(Product).where(Product.name == row['product2']))
                            all_products[row['product2']] = p
                        o.order_items.append(OrderItem(
                            unit_price=float(row['unit_price2']),
                            quantity=int(row['quantity2']),
                            product=p))
    
                    if row['product3']:
                        p = all_products.get(row['product3'])
                        if p is None:
                            p = session.scalar(select(Product).where(Product.name == row['product3']))
                            all_products[row['product3']] = p
                        o.order_items.append(OrderItem(
                            unit_price=float(row['unit_price3']),
                            quantity=int(row['quantity3']),
                            product=p))
                    
if __name__ == '__main__':
    main()
