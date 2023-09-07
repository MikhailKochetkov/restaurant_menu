import time

import pytest
from fastapi import status

from .conftest import client
from .helpers import create_unique_menu

PREFIX = '/api/v1/menus'


@pytest.mark.asyncio
async def test_get_menus(client):
    get_response = await client.get(f'{PREFIX}/')
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == []
    menu = create_unique_menu()
    post_response = await client.post(f'{PREFIX}/', json=menu)
    post_data = post_response.json()
    get_response = await client.get(f'{PREFIX}/')
    get_data = get_response.json()
    assert get_response.status_code == status.HTTP_200_OK
    assert get_data[0]['id'] == post_data['id']
    assert get_data[0]['title'] == post_data['title']
    assert get_data[0]['description'] == post_data['description']


@pytest.mark.asyncio
async def test_create_menu(client):
    menu = create_unique_menu()
    post_response = await client.post(f'{PREFIX}/', json=menu)
    post_data = post_response.json()
    assert post_response.status_code == status.HTTP_201_CREATED
    assert 'id' in post_data
    assert 'title' in post_data
    assert 'description' in post_data
    assert post_data['title'] == menu['title']
    assert post_data['description'] == menu['description']
    post_response = await client.post(f'{PREFIX}/', json=menu)
    assert post_response.status_code == status.HTTP_409_CONFLICT
    assert post_response.json()['detail'] == 'menu already exists'


@pytest.mark.asyncio
async def test_get_menu_by_id(client):
    menu = create_unique_menu()
    post_response = await client.post(f'{PREFIX}/', json=menu)
    menu_id = post_response.json()['id']
    get_response = await client.get(f'{PREFIX}/{menu_id}')
    get_data = get_response.json()
    assert get_response.status_code == status.HTTP_200_OK
    assert get_data['id'] == menu_id
    assert get_data['title'] == menu['title']
    assert get_data['description'] == menu['description']
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    get_response = await client.get(f'{PREFIX}/{menu_id}')
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'menu not found'


@pytest.mark.asyncio
async def test_update_menu(client):
    menu = create_unique_menu()
    upd_menu = {
        'title': f'updated test menu {str(time.time())}',
        'description': f'updated test menu description {str(time.time())}'
    }
    post_response = await client.post(f'{PREFIX}/', json=menu)
    menu_id = post_response.json()['id']
    patch_response = await client.patch(
        f'{PREFIX}/{menu_id}',
        json=upd_menu
    )
    patch_data = patch_response.json()
    assert patch_response.status_code == status.HTTP_200_OK
    assert patch_data['id'] == menu_id
    assert patch_data['title'] == upd_menu['title']
    assert patch_data['description'] == upd_menu['description']
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    patch_response = await client.patch(
        f'{PREFIX}/{menu_id}',
        json=upd_menu
    )
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
    assert patch_response.json()['detail'] == 'menu not found'


@pytest.mark.asyncio
async def test_delete_menu(client):
    menu = create_unique_menu()
    post_response = await client.post(f'{PREFIX}/', json=menu)
    menu_id = post_response.json()['id']
    del_response = await client.delete(f'{PREFIX}/{menu_id}')
    assert del_response.json()['message'] == 'menu deleted successfully'
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    del_response = await client.delete(f'{PREFIX}/{menu_id}')
    assert del_response.status_code == status.HTTP_404_NOT_FOUND
    assert del_response.json()['detail'] == 'menu not found'
