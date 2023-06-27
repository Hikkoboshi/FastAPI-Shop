import json

from fastapi import Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import get_async_session
from catalog.models import Product, Category
from catalog.schemas import CategoryCreate, ProductCreate, CategoryUpdate, ProductUpdate, ProductRead


# Functions to CREATE models
async def create_category(category: CategoryCreate, session: AsyncSession):
    new_category = Category(**category.dict())
    try:
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return new_category
    except IntegrityError:
        if IntegrityError:
            raise HTTPException(
                status_code=400,
                detail=f"Category with name '{category.name}' already exists"
            )


async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    new_product = Product(**product.dict())
    try:
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product
    except IntegrityError:
        if IntegrityError:
            raise HTTPException(
                status_code=404,
                detail=f"Category with name '{product.category_name}' doesn't exist"
            )


# Functions to READ models
async def get_category_by_id(category_id: int, session: AsyncSession):
    query = select(Category).where(Category.id == category_id)
    result = await session.execute(query)
    result = result.scalars().first()
    if result:
        return result
    else:
        raise HTTPException(
                status_code=404,
                detail=f"Category with id '{category_id}' doesn't exist"
            )

async def get_category_by_name(category_name: str, session: AsyncSession):
    query = select(Category).where(Category.name == category_name)
    result = await session.execute(query)
    result = result.scalars().first()
    if result:
        return result
    else:
        raise HTTPException(
                status_code=404,
                detail=f"Category with name '{category_name}' doesn't exist"
            )


async def get_categories(skip: int, limit: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Category).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


async def get_products(skip: int, limit: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()


async def get_product_by_id(product_id: int, session: AsyncSession):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    result = result.scalars().first()
    if result:
        return result
    else:
        raise HTTPException(
                status_code=404,
                detail=f"Product with name '{product_id}' doesn't exist"
            )


async def get_product_by_name(product_name: str, session: AsyncSession):
    query = select(Product).where(Product.name == product_name)
    result = await session.execute(query)
    result = result.scalars().first()
    if result:
        return result
    else:
        raise HTTPException(
                status_code=404,
                detail=f"Product with name '{product_name}' doesn't exist"
            )


async def get_categories_with_products(skip: int, limit: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Category).offset(skip).limit(limit).options(selectinload(Category.products))
    )
    return result.scalars().all()


async def get_category_products(category_name: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Product).join(Category, Category.name == category_name))
    return result.scalars().all()


# Functions to UPDATE models
async def update_category(category_id: int, category_to_update: CategoryUpdate, session: AsyncSession):
    category = await get_category_by_id(category_id, session)
    category_to_update = category_to_update.dict(exclude_unset=True)
    for key, value in category_to_update.items():
        setattr(category, key, value)
    await session.commit()
    return category


async def update_product(product_id: int, product_to_update: ProductUpdate, session: AsyncSession):
    product = await get_product_by_id(product_id, session)
    product_to_update = product_to_update.dict(exclude_unset=True)
    for key, value in product_to_update.items():
        setattr(product, key, value)
    await session.commit()
    return product


# Functions to DELETE models
async def delete_category(category_id: int, session: AsyncSession):
    category = await get_category_by_id(category_id, session)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(category)
    await session.commit()
    return {'message': 'Category deleted successfully'}


async def delete_product(product_id: int, session: AsyncSession):
    product = await get_category_by_id(product_id, session)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
    return {'message': 'Product deleted successfully'}
