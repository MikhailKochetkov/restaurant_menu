import time

import pytest
from fastapi import status

from .conftest import client
from .helpers import (
    create_unique_dish,
    create_unique_menu,
    create_unique_submenu)

PREFIX = '/api/v1/menus'


@pytest.mark.asyncio
async def test_create_dish(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    real_menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(real_menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/',
        json=submenu
    )
    real_submenu_id = submenu_response.json()['id']
    dish = create_unique_dish(real_submenu_id)
    dish_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/{real_submenu_id}/dishes/',
        json=dish
    )
    dish_data = dish_response.json()
    assert dish_response.status_code == status.HTTP_201_CREATED
    assert 'id' in dish_data
    assert 'title' in dish_data
    assert 'description' in dish_data
    assert dish_data['title'] == dish['title']
    assert dish_data['description'] == dish['description']
    assert dish_data['price'] == str(dish['price'])
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    submenu_id = real_submenu_id
    dish_response = await client.post(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}/dishes/',
        json=dish
    )
    assert dish_response.status_code == status.HTTP_404_NOT_FOUND
    assert dish_response.json()['detail'] == 'menu does not exist'
    menu_id = real_menu_id
    submenu_id = '0e0b0000-00b0-00d0-b0a0-c0e0000e0f00'
    dish_response = await client.post(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}/dishes/',
        json=dish
    )
    assert dish_response.json()['detail'] == 'submenu does not exist'


@pytest.mark.asyncio
async def test_get_dishes(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    real_menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(real_menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/',
        json=submenu
    )
    real_submenu_id = submenu_response.json()['id']
    dish = create_unique_dish(real_submenu_id)
    dish_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/{real_submenu_id}/dishes/',
        json=dish
    )
    post_resp_data = dish_response.json()
    get_dish_response = await client.get(
        f'{PREFIX}/{real_menu_id}/submenus/{real_submenu_id}/dishes/'
    )
    get_resp_data = get_dish_response.json()[0]
    assert get_dish_response.status_code == status.HTTP_200_OK
    assert get_resp_data['id'] == post_resp_data['id']
    assert get_resp_data['title'] == post_resp_data['title']
    assert get_resp_data['description'] == post_resp_data['description']
    assert get_resp_data['price'] == str(post_resp_data['price'])
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    submenu_id = real_submenu_id
    get_dish_response = await client.get(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}/dishes/'
    )
    assert get_dish_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_dish_response.json()['detail'] == 'menu does not exist'


@pytest.mark.asyncio
async def test_get_dish_by_id(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    real_menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(real_menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/',
        json=submenu
    )
    real_submenu_id = submenu_response.json()['id']
    dish = create_unique_dish(real_submenu_id)
    dish_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/{real_submenu_id}/dishes/',
        json=dish
    )
    dish_data = dish_response.json()
    real_dish_id = dish_data['id']
    get_dish_response = await client.get(
        f'{PREFIX}/{real_menu_id}'
        f'/submenus/{real_submenu_id}'
        f'/dishes/{real_dish_id}'
    )
    assert get_dish_response.status_code == status.HTTP_200_OK
    assert get_dish_response.json()['id'] == real_dish_id
    assert get_dish_response.json()['title'] == dish_data['title']
    assert get_dish_response.json()['description'] == dish_data['description']
    assert get_dish_response.json()['price'] == str(dish_data['price'])
    menu_id = real_menu_id
    submenu_id = real_submenu_id
    dish_id = '0df00000-dc0c-0000-ac0c-0f0ebb000ac0'
    get_dish_response = await client.get(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert get_dish_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_dish_response.json()['detail'] == 'dish not found'
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    submenu_id = real_submenu_id
    dish_id = real_dish_id
    get_dish_response = await client.get(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert get_dish_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_dish_response.json()['detail'] == 'menu does not exist'
    menu_id = real_menu_id
    submenu_id = '0e0b0000-00b0-00d0-b0a0-c0e0000e0f00'
    dish_id = real_dish_id
    get_dish_response = await client.get(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
    )
    assert get_dish_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_dish_response.json()['detail'] == 'submenu does not exist'


@pytest.mark.asyncio
async def test_update_dish(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    real_menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(real_menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/',
        json=submenu
    )
    real_submenu_id = submenu_response.json()['id']
    dish = create_unique_dish(real_submenu_id)
    dish_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/{real_submenu_id}/dishes/',
        json=dish
    )
    real_dish_id = dish_response.json()['id']
    upd_dish = {
        'title': f'updated test dish title {str(time.time())}',
        'description': f'updated test dish description {str(time.time())}',
        'price': 12.12,
    }
    patch_response = await client.patch(
        (f'{PREFIX}/{real_menu_id}'
         f'/submenus/{real_submenu_id}'
         f'/dishes/{real_dish_id}'),
        json=upd_dish
    )
    patch_data = patch_response.json()
    assert patch_response.status_code == status.HTTP_200_OK
    assert patch_data['id'] == real_dish_id
    assert patch_data['title'] == upd_dish['title']
    assert patch_data['description'] == upd_dish['description']
    assert patch_data['price'] == str(upd_dish['price'])
    menu_id = real_menu_id
    submenu_id = real_submenu_id
    dish_id = '0df00000-dc0c-0000-ac0c-0f0ebb000ac0'
    patch_response = await client.patch(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        json=upd_dish
    )
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
    assert patch_response.json()['detail'] == 'dish not found'
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    submenu_id = real_submenu_id
    dish_id = real_dish_id
    patch_response = await client.patch(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        json=upd_dish
    )
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
    assert patch_response.json()['detail'] == 'menu does not exist'
    menu_id = real_menu_id
    submenu_id = '0e0b0000-00b0-00d0-b0a0-c0e0000e0f00'
    dish_id = real_dish_id
    patch_response = await client.patch(
        f'{PREFIX}/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        json=upd_dish
    )
    assert patch_response.status_code == status.HTTP_404_NOT_FOUND
    assert patch_response.json()['detail'] == 'submenu does not exist'


@pytest.mark.asyncio
async def test_delete_dish(client):
    menu = create_unique_menu()
    menu_response = await client.post(f'{PREFIX}/', json=menu)
    real_menu_id = menu_response.json()['id']
    submenu = create_unique_submenu(real_menu_id)
    submenu_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/',
        json=submenu
    )
    real_submenu_id = submenu_response.json()['id']
    dish = create_unique_dish(real_submenu_id)
    dish_response = await client.post(
        f'{PREFIX}/{real_menu_id}/submenus/{real_submenu_id}/dishes/',
        json=dish
    )
    real_dish_id = dish_response.json()['id']
    menu_id = '0000b000-0e00-00d0-a000-00000be000da'
    del_response = await client.delete(
        f'{PREFIX}/{menu_id}'
        f'/submenus/{real_submenu_id}'
        f'/dishes/{real_dish_id}'
    )
    assert del_response.status_code == status.HTTP_404_NOT_FOUND
    assert del_response.json()['detail'] == 'menu does not exist'
    submenu_id = '0e0b0000-00b0-00d0-b0a0-c0e0000e0f00'
    del_response = await client.delete(
        f'{PREFIX}/{real_menu_id}'
        f'/submenus/{submenu_id}'
        f'/dishes/{real_dish_id}'
    )
    assert del_response.status_code == status.HTTP_404_NOT_FOUND
    assert del_response.json()['detail'] == 'submenu does not exist'
    del_response = await client.delete(
        f'{PREFIX}/{real_menu_id}'
        f'/submenus/{real_submenu_id}'
        f'/dishes/{real_dish_id}'
    )
    assert del_response.json()['message'] == 'dish deleted successfully'
    dish_id = '0df00000-dc0c-0000-ac0c-0f0ebb000ac0'
    del_response = await client.delete(
        f'{PREFIX}/{real_menu_id}'
        f'/submenus/{real_submenu_id}'
        f'/dishes/{dish_id}'
    )
    assert del_response.status_code == status.HTTP_404_NOT_FOUND
    assert del_response.json()['detail'] == 'dish not found'
