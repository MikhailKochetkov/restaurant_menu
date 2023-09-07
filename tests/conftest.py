import asyncio
import pytest
import pytest_asyncio

from httpx import AsyncClient
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker)

from main import app
from db.models import Base
from db.db_connection import TEST_CONNECTION_STRING
from db.session import get_session


test_engine = create_async_engine(
    TEST_CONNECTION_STRING, echo=True, poolclass=NullPool
)

test_async_session = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_session() -> AsyncSession:
    async with test_async_session() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


asyncio.run(prepare_database())


@pytest_asyncio.fixture(scope='session', autouse=True)
async def clean_up_database():
    yield
    await drop_database()


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def client(event_loop):
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
