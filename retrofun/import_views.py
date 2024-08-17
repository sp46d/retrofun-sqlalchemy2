import os
import csv
from sqlalchemy import select, delete
from uuid import UUID
from retrofun.db import Session
from retrofun.models import Customer, BlogArticle, BlogUser, BlogSession, BlogView
from datetime import datetime


def main():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'views.csv')
    
    with Session() as session:
        with session.begin():
            session.execute(delete(BlogUser))
            session.execute(delete(BlogSession))
            session.execute(delete(BlogView))
            
    with Session() as session:
        all_users: dict[str, BlogUser] = {}
        all_customers: dict[str, Customer | None] = {}
        all_sessions: dict[str, BlogSession] = {}
        all_articles: dict[str, BlogArticle | None] = {}
        with open(data_path) as f:
            reader = csv.DictReader(f)
            i: int = 0
            for row in reader:
                user = all_users.get(row['user'])
                if user is None:
                    customer: Customer | None = None
                    if row['customer']:
                        customer = all_customers.get(row['customer'])
                        if customer is None:
                            customer = session.scalar(select(Customer).where(Customer.name == row['customer']))
                            all_customers[row['customer']] = customer
                    user = BlogUser(id=UUID(hex=row['user']),
                                    customer=customer)
                    session.add(user)
                    all_users[row['user']] = user
                    
                blog_session = all_sessions.get(row['session'])
                if blog_session is None:
                    blog_session = BlogSession(id=UUID(hex=row['session']),
                                               user=user)
                    session.add(blog_session)
                    all_sessions[row['session']] = blog_session
                
                article = all_articles.get(row['title'])
                if article is None:
                    article = session.scalar(select(BlogArticle).where(BlogArticle.title == row['title']))
                    all_articles[row['title']] = article
                view = BlogView(timestamp=datetime.strptime(row['timestamp'],
                                                            '%Y-%m-%d %H:%M:%S'),
                                article=article,
                                session=blog_session)
                session.add(view)
                
                i += 1
                if i % 100 == 0:
                    print(i)
                    session.commit()
            print(i)
            session.commit()
                    

if __name__ == '__main__':
    main()