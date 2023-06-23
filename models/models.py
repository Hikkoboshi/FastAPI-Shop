from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship, declarative_base



Base = declarative_base()


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String)

    products = relationship("Product", backref="category")


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    category_name = Column(String, ForeignKey('category.name'), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    slug = Column(String)
