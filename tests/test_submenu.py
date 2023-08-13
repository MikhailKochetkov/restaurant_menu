import pytest

from fastapi import status

from .conftest import client
from .helpers import (
    create_unique_menu,
    create_unique_submenu)


@pytest.mark.asyncio
async def test_create_submenu(client):
    menu = create_unique_menu()
    menu_response = await client.post('/api/v1/menus', json=menu)
    menu_id = menu_response.json()["id"]
    submenu = create_unique_submenu(menu_id)
    submenu_response = await client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu)
    submenu_data = submenu_response.json()
    assert submenu_response.status_code == status.HTTP_201_CREATED
    assert 'id' in submenu_data
    assert 'title' in submenu_data
    assert 'description' in submenu_data
    assert submenu_data['title'] == submenu["title"]
    assert submenu_data['description'] == submenu["description"]
    menu_id = "1aa-2bb"
    submenu = create_unique_submenu(menu_id)
    submenu_response = await client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu)
    assert submenu_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_submenus(client):
    menu = create_unique_menu()
    menu_response = await client.post('/api/v1/menus', json=menu)
    menu_id = menu_response.json()["id"]
    submenu = create_unique_submenu(menu_id)
    submenu_response = await client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu)
    get_submenu_response = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert get_submenu_response.status_code == status.HTTP_200_OK
    assert get_submenu_response.json()[0]["id"] == submenu_response.json()["id"]
    assert get_submenu_response.json()[0]["title"] == submenu_response.json()["title"]
    assert get_submenu_response.json()[0]["description"] == submenu_response.json()["description"]


@pytest.mark.asyncio
async def test_get_submenu_by_id(client):
    menu = create_unique_menu()
    menu_response = await client.post('/api/v1/menus', json=menu)
    menu_id = menu_response.json()["id"]
    submenu = create_unique_submenu(menu_id)
    submenu_response = await client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu)
    submenu_id = submenu_response.json()["id"]
    get_submenu_response = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert get_submenu_response.status_code == status.HTTP_200_OK
    assert get_submenu_response.json()["id"] == submenu_response.json()["id"]
    assert get_submenu_response.json()["title"] == submenu_response.json()["title"]
    assert get_submenu_response.json()["description"] == submenu_response.json()["description"]


@pytest.mark.skip(reason='no way of currently testing this')
@pytest.mark.asyncio
async def test_update_submenu(client):
    pass


@pytest.mark.skip(reason='no way of currently testing this')
@pytest.mark.asyncio
async def test_delete_submenu():
    pass
