from typing import List

import aiohttp
from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from catalog import crud
from models.models import User, Category, Product
from database import get_async_session
from auth.auth import auth_backend
from auth.manager import get_user_manager
from schemas.schemas import CategoryCreate, CategoryRead, ProductCreate, ProductRead, CategoryProductsRead

router = APIRouter()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)


@router.post('/category/', response_model=CategoryRead)
async def create_category(category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    return await crud.create_category(category, session)


@router.get('/category/{category_name}', response_model=CategoryProductsRead)
async def get_category(category_name: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Category).where(Category.name == category_name))
    return result.scalars().first()


@router.get('/category/products/')
async def get_category_products(category_name: str, session: AsyncSession = Depends(get_async_session)):
    return await crud.get_category_products(category_name, session)


@router.post('/product/', response_model=ProductRead)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        return await crud.create_product(product, session)
    except:
        raise HTTPException(status_code=404, detail=f"Something wrong...")


@router.get('/products/', response_model=List[ProductRead])
async def get_products(skip: int = 0, limit: int = 5, session: AsyncSession = Depends(get_async_session)):
    return await crud.get_products(skip, limit, session)


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

