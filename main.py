from fastapi import FastAPI, APIRouter

from api.menu_handlers import menu_router
from api.submenu_handlers import submenu_router
from api.dish_handlers import dish_router


app = FastAPI(title='Restaurant menu')
main_router = APIRouter()

main_router.include_router(menu_router)
main_router.include_router(submenu_router)
main_router.include_router(dish_router)
app.include_router(main_router)
