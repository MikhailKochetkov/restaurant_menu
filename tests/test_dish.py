import pytest

from fastapi import status

from .conftest import client
from .helpers import (
    create_unique_menu,
    create_unique_submenu,
    create_unique_dish)


@pytest.mark.asyncio
async def test_create_dish(client):
    menu = create_unique_menu()
    menu_response = await client.post('/api/v1/menus', json=menu)
    real_menu_id = menu_response.json()["id"]
    submenu = create_unique_submenu(real_menu_id)
    submenu_response = await client.post(
        f'/api/v1/menus/{real_menu_id}/submenus',
        json=submenu
    )
    real_submenu_id = submenu_response.json()["id"]
    dish = create_unique_dish(real_submenu_id)
    dish_response = await client.post(
        f'/api/v1/menus/{real_menu_id}/submenus/{real_submenu_id}/dishes',
        json=dish
    )
    dish_data = dish_response.json()
    assert dish_response.status_code == status.HTTP_201_CREATED
    assert 'id' in dish_data
    assert 'title' in dish_data
    assert 'description' in dish_data
    assert dish_data['title'] == dish["title"]
    assert dish_data['description'] == dish["description"]
    assert dish_data['price'] == str(dish["price"])
    menu_id = "44-yy-ww"
    submenu_id = real_submenu_id
    dish_response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json=dish
    )
    assert dish_response.status_code == status.HTTP_404_NOT_FOUND
    assert dish_response.json()["detail"] == "menu does not exist"
    menu_id = real_menu_id
    submenu_id = "33-oo-5"
    dish_response = await client.post(
        f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
        json=dish
    )
    assert dish_response.json()["detail"] == "submenu does not exist"


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
