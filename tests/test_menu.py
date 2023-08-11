import pytest

from fastapi import status

from .conftest import client


@pytest.mark.asyncio
async def test_create_menu(client):
    data = {
        "title": "test menu 1",
        "description": "test menu description 1"
    }

    response = await client.post('/api/v1/menus', json=data)
    menu_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in menu_data
    assert 'title' in menu_data
    assert 'description' in menu_data
    assert menu_data['title'] == data["title"]
    assert menu_data['description'] == data["description"]

    response = await client.post('/api/v1/menus', json=data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "menu already exists"


@pytest.mark.asyncio
async def test_get_menus(client):
    response = await client.get('/api/v1/menus')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_menu_by_id(client):
    data = {
        "title": "test menu 2",
        "description": "test menu description 2"
    }

    post_response = await client.post('/api/v1/menus', json=data)
    menu_id = post_response.json()["id"]
    get_response = await client.get(f'/api/v1/menus/{menu_id}')
    menu_data = get_response.json()
    assert get_response.status_code == status.HTTP_200_OK
    assert menu_data["id"] == menu_id
    assert menu_data["title"] == data["title"]
    assert menu_data["description"] == data["description"]


@pytest.mark.asyncio
async def test_update_menu(client):
    data = {
        "title": "test menu 3",
        "description": "test menu description 3"
    }
    upd_data = {
        "title": "updated test menu 3",
        "description": "updated test menu description 3"
    }

    post_response = await client.post('/api/v1/menus', json=data)
    menu_id = post_response.json()["id"]
    patch_response = await client.patch(f'/api/v1/menus/{menu_id}', json=upd_data)
    patch_data = patch_response.json()
    assert patch_response.status_code == status.HTTP_200_OK
    assert patch_data["id"] == menu_id
    assert patch_data["title"] == upd_data["title"]
    assert patch_data["description"] == upd_data["description"]

    menu_id = "1"
    patch_response = await client.patch(f'/api/v1/menus/{menu_id}', json=upd_data)
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_menu(client):
    data = {
        "title": "test menu 4",
        "description": "test menu description 4"
    }

    post_response = await client.post('/api/v1/menus', json=data)
    menu_id = post_response.json()["id"]
    del_response = await client.delete(f'/api/v1/menus/{menu_id}')
    assert del_response.json()["message"] == "menu deleted successfully"

    menu_id = "2"
    del_response = await client.delete(f'/api/v1/menus/{menu_id}')
    assert del_response.status_code == status.HTTP_404_NOT_FOUND
