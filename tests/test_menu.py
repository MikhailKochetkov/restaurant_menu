import pytest

from fastapi import status

from .conftest import client


@pytest.mark.asyncio
async def test_create_menu(client):
    menu_data = {
        "title": "test menu",
        "description": "test menu description"
    }
    response = await client.post('/api/v1/menus', json=menu_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert response.json()['title'] == 'test menu'
    assert response.json()['description'] == 'test menu description'

    response = await client.post('/api/v1/menus', json=menu_data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "menu already exists"


@pytest.mark.asyncio
async def test_get_menus(client):
    response = await client.get('/api/v1/menus')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_menu_by_id(client):
    menu_data = {
        "title": "new test menu",
        "description": "new test menu description"
    }
    post_response = await client.post('/api/v1/menus', json=menu_data)

    menu_id = post_response.json()["id"]
    get_response = await client.get(f'/api/v1/menus/{menu_id}')
    data = get_response.json()
    assert get_response.status_code == status.HTTP_200_OK
    assert data["id"] == menu_id
    assert data["title"] == menu_data["title"]
    assert data["description"] == menu_data["description"]
#
#
# @pytest.mark.asyncio
# async def test_update_menu(client):
#     pass
#
#
# @pytest.mark.asyncio
# async def test_delete_menu(client):
#     pass
