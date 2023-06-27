from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Relationship, declarative_base

from core.settings import BaseMixinIntegerID

CatalogBase = declarative_base(cls=BaseMixinIntegerID)


class Category(CatalogBase):
    name = Column(String, unique=True, nullable=False)
    slug = Column(String)


class Product(CatalogBase):
    category_name = Column(String, ForeignKey('category.name'), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    slug = Column(String)

    category = Relationship('Category')
