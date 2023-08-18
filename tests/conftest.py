import pytest
import pytest_asyncio
import asyncio

from httpx import AsyncClient

#from main import app


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def client(event_loop):
    async with AsyncClient(base_url="http://app:8000") as ac:
        yield ac
