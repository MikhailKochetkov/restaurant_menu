from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .db_connection import PG_CONNECTION_STRING
from settings import DEV_MODE


if DEV_MODE:
    engine = create_async_engine(PG_CONNECTION_STRING, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def get_session():
        async with async_session() as session:
            yield session
