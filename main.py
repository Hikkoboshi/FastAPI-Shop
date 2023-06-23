from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from crud.crud import get_products
from database import get_async_session
from routes.router import fastapi_users, router
from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate, UserUpdate


app = FastAPI()


templates = Jinja2Templates(directory="templates")


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
async def catalog(request: Request, skip: int = 0, limit: int = 6, session: AsyncSession = Depends(get_async_session)):
    products = await get_products(skip, limit, session)
    previous_page = skip - 1 if skip >= 0 else None
    next_page = skip + 1
    pagination = {
        'previous': previous_page,
        'next': next_page,
        'pages': 5
    }
    return templates.TemplateResponse('ProductsList.html',
                                      {'request': request, 'products': products, 'pagination': pagination})
