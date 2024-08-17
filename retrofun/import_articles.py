import os
import csv
from sqlalchemy import select, delete
from retrofun.db import Session
from retrofun.models import Product, BlogArticle, BlogAuthor
from datetime import datetime

def main():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'articles.csv')
    
    with Session() as session:
        with session.begin():
            session.execute(delete(BlogArticle))
            session.execute(delete(BlogAuthor))
            
    with Session() as session:
        with session.begin():
            all_authors: dict[str, BlogAuthor] = {}
            all_products: dict[str, Product | None] = {}
            
            with open(data_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    author = all_authors.get(row['author'])
                    if author is None:
                        author = BlogAuthor(name=row['author'])
                        all_authors[row['author']] = author
                        
                    product = None
                    if row['product']:
                        product = all_products.get(row['product'])
                        if product is None:
                            product = session.scalar(select(Product).where(Product.name == row['product']))
                            all_products[row['product']] = product
                    article = BlogArticle(title=row['title'],
                                          product=product,
                                          author=author,
                                          timestamp=datetime.strptime(row['timestamp'],
                                                                      '%Y-%m-%d %H:%M:%S'))
                    session.add(article)
                    
                    
if __name__ == '__main__':
    main()