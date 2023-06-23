from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from models.models import Product, Category
from schemas.schemas import CategoryCreate, ProductCreate, CategoryRead, ProductRead


async def get_products(skip: int, limit: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()


async def get_categories(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Category))
    return result.scalars().all()


async def get_category_products(category_name: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Product).join(Category, Category.name == category_name))
    return result.scalars().all()


async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    new_category = Category(**category.dict())
    try:
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return new_category
    except Exception:
        raise HTTPException(status_code=400, detail=f"Category {category.name} already exist!")


async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    new_product = Product(**product.dict())
    try:
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product
    except HTTPException:
        raise HTTPException(status_code=400, detail=f"Product {product.name} already exist!")
