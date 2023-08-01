import asyncio
from fastapi import FastAPI, APIRouter

from api.menu_handlers import menu_router
from api.submenu_handlers import submenu_router
from api.dish_handlers import dish_router
from settings import DEV_MODE


app = FastAPI(title='Restaurant menu')
main_router = APIRouter()

main_router.include_router(menu_router)
main_router.include_router(submenu_router)
main_router.include_router(dish_router)
app.include_router(main_router)

if not DEV_MODE:
    from db.session import create_tables

    asyncio.create_task(create_tables())
