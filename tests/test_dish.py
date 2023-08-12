import pytest

from fastapi import status

from .conftest import client


@pytest.mark.skip(reason='no way of currently testing this')
@pytest.mark.asyncio
async def test_create_dish(client):
    pass


@pytest.mark.skip(reason='no way of currently testing this')
@pytest.mark.asyncio
async def test_get_dishes(client):
    pass


@pytest.mark.skip(reason='no way of currently testing this')
@pytest.mark.asyncio
async def test_get_dish_by_id(client):
    pass


@pytest.mark.skip(reason='no way of currently testing this')
@pytest.mark.asyncio
async def test_update_dish(client):
    pass


@pytest.mark.skip(reason='no way of currently testing this')
@pytest.mark.asyncio
async def test_delete_dish(client):
    pass
