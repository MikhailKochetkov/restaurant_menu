from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from .models import Menu, SubMenu, Dish
from .db_connection import CONNECTION_STRING, PG_CONNECTION_STRING
from settings import DEV_MODE


if DEV_MODE:
    engine = create_engine(
        CONNECTION_STRING,
        connect_args={"check_same_thread": False}
    )
    Menu.metadata.create_all(engine)
    SubMenu.metadata.create_all(engine)
    Dish.metadata.create_all(engine)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
else:
    engine = create_async_engine(PG_CONNECTION_STRING, future=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Menu.metadata.create_all)
            await conn.run_sync(SubMenu.metadata.create_all)
            await conn.run_sync(Dish.metadata.create_all)

    async def get_session():
        async with async_session() as session:
            yield session
