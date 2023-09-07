import time

import pytest
from fastapi import status

from .conftest import client
from .helpers import create_unique_menu, create_unique_submenu

PREFIX = '/api/v1/menus'


@pytest.mark.asyncio
async def test_create_submenu(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{menu_id}/submenus/',
        json=submenu
    )
    submenu_data = submenu_response.json()
    assert submenu_response.status_code == status.HTTP_201_CREATED
    assert 'id' in submenu_data
    assert 'title' in submenu_data
    assert 'description' in submenu_data
    assert submenu_data['title'] == submenu['title']
    assert submenu_data['description'] == submenu['description']
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    submenu = create_unique_submenu(menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{menu_id}/submenus/',
        json=submenu
    )
    assert submenu_response.status_code == status.HTTP_404_NOT_FOUND
    assert submenu_response.json()['detail'] == 'menu does not exist'


@pytest.mark.asyncio
async def test_get_submenus(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{menu_id}/submenus/',
        json=submenu
    )
    post_resp_data = submenu_response.json()
    get_submenu_response = await client.get(
        f'{PREFIX}/{menu_id}/submenus/'
    )
    get_resp_data = get_submenu_response.json()[0]
    assert get_submenu_response.status_code == status.HTTP_200_OK
    assert get_resp_data['id'] == post_resp_data['id']
    assert get_resp_data['title'] == post_resp_data['title']
    assert get_resp_data['description'] == post_resp_data['description']


@pytest.mark.asyncio
async def test_get_submenu_by_id(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    real_menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(real_menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/',
        json=submenu
    )
    post_resp_data = submenu_response.json()
    real_submenu_id = submenu_response.json()['id']
    get_response = await client.get(
        f'{PREFIX}/{real_menu_id}/submenus/{real_submenu_id}'
    )
    get_resp_data = get_response.json()
    assert get_response.status_code == status.HTTP_200_OK
    assert get_resp_data['id'] == post_resp_data['id']
    assert get_resp_data['title'] == post_resp_data['title']
    assert get_resp_data['description'] == post_resp_data['description']
    submenu_id = '0000b000-0e00-00d0-a000-00000be000da'
    get_response = await client.get(
        f'{PREFIX}/{real_menu_id}/submenus/{submenu_id}'
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json()['detail'] == 'submenu not found'


@pytest.mark.asyncio
async def test_update_submenu(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    real_menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(real_menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/',
        json=submenu
    )
    real_submenu_id = submenu_response.json()['id']
    upd_submenu = {
        'title': f'updated test submenu title {str(time.time())}',
        'description': f'updated est submenu description {str(time.time())}'
    }
    patch_response = await client.patch(
        f'{PREFIX}/{real_menu_id}/submenus/{real_submenu_id}',
        json=upd_submenu
    )
    patch_data = patch_response.json()
    assert patch_response.status_code == status.HTTP_200_OK
    assert patch_data['id'] == real_submenu_id
    assert patch_data['title'] == upd_submenu['title']
    assert patch_data['description'] == upd_submenu['description']
    menu_id = real_menu_id
    submenu_id = '0000b000-0e00-00d0-a000-00000be000da'
    patch_response = await client.patch(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}',
        json=upd_submenu
    )
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
    assert patch_response.json()['detail'] == 'submenu not found'
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    submenu_id = real_submenu_id
    patch_response = await client.patch(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}',
        json=upd_submenu
    )
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
    assert patch_response.json()['detail'] == 'menu does not exist'


@pytest.mark.asyncio
async def test_delete_submenu(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    real_menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(real_menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/',
        json=submenu
    )
    real_submenu_id = submenu_response.json()['id']
    del_response = await client.delete(
        f'/api/v1/menus/{real_menu_id}/submenus/{real_submenu_id}'
    )
    assert del_response.json()['message'] == 'submenu deleted successfully'
    submenu_id = '0000b000-0e00-00d0-a000-00000be000da'
    del_response = await client.delete(
        f'{PREFIX}/{real_menu_id}/submenus/{submenu_id}'
    )
    assert del_response.status_code == status.HTTP_404_NOT_FOUND
    assert del_response.json()['detail'] == 'submenu not found'
