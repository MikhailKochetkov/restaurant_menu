import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient

from main import app


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def client(event_loop):
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
