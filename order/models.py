from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

from core.settings import BaseMixinIntegerID
from catalog.models import Product

OrderBase = declarative_base(cls=BaseMixinIntegerID)


class Order(OrderBase):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    total = Column(Float)


class OrderItems(OrderBase):
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship(Order)
    product = relationship(Product)
