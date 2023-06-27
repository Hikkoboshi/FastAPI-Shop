from typing import List

from catalog.schemas import ProductRead
from core.settings import BaseSchemaModel


class OrderRead(BaseSchemaModel):
    id: int
    first_name: str
    last_name: str
    email: float
    phone: str
    address: str
    total: float


class OrderProductsRead(OrderRead):
    products: List[ProductRead] = []


class OrderCreate(BaseSchemaModel):
    first_name: str
    last_name: str
    email: float
    phone: str
    address: str
    total: float
