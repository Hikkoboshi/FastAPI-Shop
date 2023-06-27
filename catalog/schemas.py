from typing import List

from core.settings import BaseSchemaModel


class CategoryRead(BaseSchemaModel):
    id: int | None
    name: str
    slug: str | None


class CategoryCreate(BaseSchemaModel):
    name: str


class CategoryUpdate(BaseSchemaModel):
    name: str


class ProductRead(BaseSchemaModel):
    id: int
    category_name: str | None
    name: str
    price: float


class ProductCreate(BaseSchemaModel):
    category_name: str
    name: str
    price: float


class ProductUpdate(BaseSchemaModel):
    category_name: str | None
    name: str | None
    price: float | None


class CategoryProductsRead(CategoryRead):
    products: List[ProductRead] = []
