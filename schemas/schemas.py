from typing import List

from pydantic import BaseModel


class AppBaseModel(BaseModel):
    class Config:
        orm_mode = True


class CategoryRead(AppBaseModel):
    id: int | None
    name: str
    slug: str | None


class CategoryCreate(AppBaseModel):
    name: str


class ProductRead(AppBaseModel):
    id: int
    category_name: str | None
    name: str
    price: float


class ProductCreate(AppBaseModel):
    category_name: str
    name: str
    price: float


class CategoryProductsRead(CategoryRead):
    product: List[ProductRead] = []
