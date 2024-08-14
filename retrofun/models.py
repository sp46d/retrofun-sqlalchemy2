from sqlalchemy import String, Integer, ForeignKey, Table, Column, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy.orm import WriteOnlyMapped
from retrofun.db import Model
from typing import Optional, List


# Join table between products and countries (many-to-many relationships)
ProductCountry = Table(
    'products_countries',
    Model.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), nullable=False, primary_key=True),
    Column('country_id', Integer, ForeignKey('countries.id'), nullable=False, primary_key=True)
)


# many side of one-to-many relationship
class Product(Model):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    manufacturer_id: Mapped[Optional[int]] = mapped_column(ForeignKey('manufacturers.id'))
    year: Mapped[int] = mapped_column(index=True)
    cpu: Mapped[Optional[str]] = mapped_column(String(32))
    
    manufacturer: Mapped['Manufacturer'] = relationship(back_populates='products')
    countries: Mapped[List['Country']] = relationship(secondary=ProductCountry, back_populates='products')
    order_items: WriteOnlyMapped['OrderItem'] = relationship(back_populates='product')
    reviews: WriteOnlyMapped['ProductReview'] = relationship(back_populates='product')
    articles: WriteOnlyMapped['BlogArticle'] = relationship(back_populates='product')
    
    def __repr__(self):
        return f'Product({self.id}, "{self.name}")'
    

# one side of one-to-many relationship
class Manufacturer(Model):
    __tablename__ = 'manufacturers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    
    products: Mapped[List['Product']] = relationship(back_populates='manufacturer', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f'Manufacturer({self.id}, "{self.name}")'
    

# many-to-many relationship with Product
class Country(Model):
    __tablename__ = 'countries'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    
    products: Mapped[List['Product']] = relationship(secondary=ProductCountry, back_populates='countries')
    
    def __repr__(self) -> str:
        return f'Country({self.id}, "{self.name})'
    

class Order(Model):
    __tablename__ = 'orders'
    
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), index=True)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey('customers.id'), index=True)
    
    customer: Mapped['Customer'] = relationship(back_populates='orders')
    order_items: Mapped[List['OrderItem']] = relationship(back_populates='order')
    
    
    def __repr__(self):
        return f'Order({self.id.hex})'
    

class Customer(Model):
    __tablename__ = 'customers'
    
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    address: Mapped[Optional[str]] = mapped_column(String(128))
    phone: Mapped[Optional[str]] = mapped_column(String(32))
    
    orders: WriteOnlyMapped['Order'] = relationship(back_populates='customer')
    product_reviews: WriteOnlyMapped['ProductReview'] = relationship(back_populates='customer')
    blog_users: WriteOnlyMapped['BlogUser'] = relationship(back_populates='customer')
    
    def __repr__(self):
        return f'Customer({self.id.hex}, "{self.name}")'
    
    
class OrderItem(Model):
    __tablename__ = 'orders_items'
    
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)
    order_id: Mapped[UUID] = mapped_column(ForeignKey('orders.id'), primary_key=True)
    unit_price: Mapped[float]
    quantity: Mapped[int]
    
    product: Mapped['Product'] = relationship(back_populates='order_items')
    order: Mapped['Order'] = relationship(back_populates='order_items')
    
    
class ProductReview(Model):
    __tablename__ = 'products_reviews'
    
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), primary_key=True)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey('customers.id'), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), index=True)
    rating: Mapped[int]
    comment: Mapped[Optional[str]] = mapped_column(Text)
    
    product: Mapped['Product'] = relationship(back_populates='reviews')
    customer: Mapped['Customer'] = relationship(back_populates='product_reviews')


class BlogArticle(Model):
    __tablename__ = 'blog_articles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('blog_authors.id'), index=True)
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey('products.id'), index=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), index=True)
    
    author: Mapped['BlogAuthor'] = relationship(back_populates='articles')
    product: Mapped[Optional['Product']] = relationship(back_populates='blog_articles')
    views: WriteOnlyMapped['BlogView'] = relationship(back_populates='article')
    
    def __repr__(self):
        return f'BlogArticle({self.id}, "{self.title}")'
    
    
class BlogAuthor(Model):
    __tablename__ = 'blog_authors'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True)
    
    articles: WriteOnlyMapped['BlogArticle'] = relationship(back_populates='author')

    def __repr__(self):
        return f'BlogAuthor({self.id}, "{self.name}")'
    
    
class BlogUser(Model):
    __tablename__ = 'blog_users'
    
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    customer_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('customers.id'), index=True)
    
    customer: Mapped[Optional['Customer']] = relationship(back_populates='blog_users')
    sessions: WriteOnlyMapped['BlogSession'] = relationship(back_populates='user')
    
    def __repr__(self):
        return f'BlogUser({self.id.hex})'
    

class BlogSession(Model):
    __tablename__ = 'blog_sessions'
    
    id: Mapped[UUID] = mapped_column(defulat=uuid4, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('blog_users.id'), index=True)
    
    user: Mapped['BlogUser'] = relationship(back_populates='sessions')
    views: WriteOnlyMapped['BlogView'] = relationship(back_populates='session')
    
    def __repr__(self):
        return f'BlogSession({self.id.hex})'
    
    
class BlogView(Model):
    __tablename__ = 'blog_views'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped['BlogArticle'] = mapped_column(ForeignKey('blog_articles.id'), index=True)
    session_id: Mapped['BlogSession'] = mapped_column(ForeignKey('blog_sessions.id'), index=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), index=True)
    
    article: Mapped['BlogArticle'] = relationship(back_populates='views')
    session: Mapped['BlogSession'] = relationship(back_populates='views')
    
    