from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
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