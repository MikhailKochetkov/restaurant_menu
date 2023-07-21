from fastapi import FastAPI, APIRouter

from api.handlers import router


app = FastAPI(title='Create restaurant menu')
main_router = APIRouter()

main_router.include_router(router)
app.include_router(main_router)
