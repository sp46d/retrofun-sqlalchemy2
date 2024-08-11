from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from retrofun.db import Model
from typing import Optional, List


# many side of one-to-many relationship
class Product(Model):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey('manufacturers.id'))
    year: Mapped[int] = mapped_column(index=True)
    country: Mapped[Optional[str]] = mapped_column(String(32))
    cpu: Mapped[Optional[str]] = mapped_column(String(32))
    
    manufacturer: Mapped['Manufacturer'] = relationship(back_populates='products')
    
    def __repr__(self):
        return f'Product({self.id}, "{self.name}")'
    

# one side of one-to-many relationship
class Manufacturer(Model):
    __tablename__ = 'manufacturers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    
    products: Mapped[List['Product']] = relationship(back_populates='manufacturer')
    
    def __repr__(self) -> str:
        return f'Manufacturer({self.id}, "{self.name}")'