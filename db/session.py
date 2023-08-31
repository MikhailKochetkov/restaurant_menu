from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine)

from settings import DEV_MODE
from .db_connection import PG_CONNECTION_STRING

if DEV_MODE:
    engine = create_async_engine(PG_CONNECTION_STRING, pool_pre_ping=True)
    async_session = async_sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )

    async def get_session() -> AsyncSession:
        async with async_session() as session:
            yield session
