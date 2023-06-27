import json
from math import ceil

from _decimal import Decimal
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from basket.basket import Basket
from catalog.crud import get_products, get_product_by_id
from catalog.models import Product
from catalog.schemas import ProductRead
from core.database import get_async_session
from catalog.router import router
from order.models import Order
from order.schemas import OrderRead, OrderCreate
from user.auth import fastapi_users, auth_backend
from user.schemas import UserRead, UserCreate, UserUpdate


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="SECRET")

templates = Jinja2Templates(directory="templates")
templates.env.globals['basket'] = Basket
templates.env.globals['messages'] = []


app.include_router(router, tags=['Catalog'])
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)


@app.get('/', response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse('MainPage.html', {'request': request, 'message': 'Hello, World!'})


@app.get('/catalog', response_class=HTMLResponse)
async def catalog(request: Request, skip: int = 1, limit: int = 6, session: AsyncSession = Depends(get_async_session)):
    products = await get_products(skip - 1, limit, session)
    previous_page = skip - 1 if skip >= 1 else None
    next_page = skip + 1
    pages = await session.execute(select(Product))
    pagination = {
        'previous': previous_page,
        'next': next_page,
        'pages': ceil(len(pages.all()) // 6)
    }
    return templates.TemplateResponse(
        'ProductsList.html',
        {'request': request, 'products': products, 'pagination': pagination}
    )


@app.get('/basket', response_class=HTMLResponse)
async def basket_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    basket = Basket(request)
    for key, value in basket.basket.items():
        product = await get_product_by_id(int(key), session)
        product = ProductRead(
            id=product.id,
            category_name=product.category_name,
            name=product.name,
            price=product.price
        )
        basket.basket[key]['product'] = product.dict()
        basket.basket[key]['total_price'] = float(basket.basket[key]["price"]) * float(basket.basket[key]["quantity"])
    return templates.TemplateResponse(
        'BasketPage.html',
        {'request': request, 'basket': basket.basket}
    )


@app.post('/basket/add')
async def basket_add(request: Request, session: AsyncSession = Depends(get_async_session)):
    basket = Basket(request)
    data = await request.form()
    product_id = int(data['product_id'])
    quantity = int(data['product_quantity'])
    product = await get_product_by_id(product_id, session)
    basket.add(product=product, quantity=quantity)
    request.session['messages'] = {'success': 'Product added to basket!'}
    response = {
        'success': 'Product added to basket!'
    }
    return response


@app.get('/order', response_class=HTMLResponse)
async def order_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    basket = Basket(request)
    return templates.TemplateResponse(
        'OrderPage.html',
        {'request': request, 'basket': basket}
    )

@app.post('/order')
async def order_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    basket = Basket(request)
    data = await request.form()
    order = Order(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        address=f"{data['address_1']}, "
                f"{data['address_2']}, "
                f"{data['city']}, "
                f"{data['region']}, "
                f"{data['post']}, "
                f"{data['country']}",
        total=basket.get_total_price()
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return RedirectResponse(url='/order/created')


@app.post('/order/created', response_class=HTMLResponse)
async def order_created_page(request: Request):
    return templates.TemplateResponse(
        'OrderCreated.html',
        {'request': request}
    )