from typing import List

import aiohttp
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_async_session
from catalog import crud
from catalog.models import Category, Product
from catalog.schemas import CategoryCreate, CategoryRead, ProductCreate, ProductRead, CategoryProductsRead, \
    CategoryUpdate, ProductUpdate
from user.auth import current_superuser

router = APIRouter()


# Category routes
@router.post('/category/',
             response_model=CategoryRead,
             dependencies=[Depends(current_superuser)]
             )
async def create_category(
        category: CategoryCreate,
        session: AsyncSession = Depends(get_async_session)
        ):
    return await crud.create_category(category, session)


@router.get('/categories/', response_model=List[CategoryRead])
async def get_categories(
        skip: int = 0,
        limit: int = 10,
        session: AsyncSession = Depends(get_async_session)):
    return await crud.get_categories(skip, limit, session)


@router.get('/categories/products', response_model=List[CategoryProductsRead])
async def get_categories_with_products(
        skip: int = 0,
        limit: int = 10,
        session: AsyncSession = Depends(get_async_session)):
    return await crud.get_categories_with_products(skip, limit, session)


@router.get('/category/{category_name}', response_model=CategoryRead)
async def get_category(category_name: str, session: AsyncSession = Depends(get_async_session)):
    result = await crud.get_category_by_name(category_name, session)
    return result


@router.get('/category/{category_name}/products/')
async def get_category_products(category_name: str, session: AsyncSession = Depends(get_async_session)):
    return await crud.get_category_products(category_name, session)


@router.put('/category/{category_id}', response_model=CategoryRead)
async def update_category(category_id: int, category: CategoryUpdate, session: AsyncSession = Depends(get_async_session)):
    return await crud.update_category(category_id, category, session)


@router.delete('/category/{category_id}')
async def delete_category(category_id: int, session: AsyncSession = Depends(get_async_session)):
    return await crud.delete_category(category_id, session)


@router.post('/product/',
             response_model=ProductRead,
             #dependencies=[Depends(current_superuser)]
             )
async def create_product(
        product: ProductCreate,
        session: AsyncSession = Depends(get_async_session)
        ):
    return await crud.create_product(product, session)


@router.get('/products/', response_model=List[ProductRead])
async def get_products(skip: int = 0, limit: int = 5, session: AsyncSession = Depends(get_async_session)):
    return await crud.get_products(skip, limit, session)


@router.put('/product/{product_id}', response_model=ProductRead)
async def update_category(product_id: int, product: ProductUpdate, session: AsyncSession = Depends(get_async_session)):
    return await crud.update_product(product_id, product, session)


@router.delete('/product/{product_id}')
async def delete_category(product_id: int, session: AsyncSession = Depends(get_async_session)):
    return await crud.delete_product(product_id, session)


# Route to get fake categories and products and fill database with them
@router.post('/fetch_fake_products')
async def fetch_fake_products(session: AsyncSession = Depends(get_async_session)):
    async with aiohttp.ClientSession() as api_session:
        async with api_session.get('https://fakestoreapi.com/products/categories') as response:
            for category in await response.json():
                new_category = Category(name=category)
                try:
                    session.add(new_category)
                    await session.commit()
                    await session.refresh(new_category)
                except:
                    raise HTTPException(status_code=400, detail=f"Category {category} already exist!")

        async with api_session.get('https://fakestoreapi.com/products') as response:
            for product in await response.json():
                new_product = Product(category_name=product['category'], name=product['title'], price=product['price'])
                try:
                    session.add(new_product)
                    await session.commit()
                    await session.refresh(new_product)
                except:
                    raise HTTPException(status_code=400, detail=f"Product {product['title']} already exist!")

