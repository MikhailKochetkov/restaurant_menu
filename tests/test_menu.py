from fastapi import status
from fastapi.testclient import TestClient

from main import app
from db.session import get_db
from db.models import Menu

client = TestClient(app)
request_data = {"title": "test menu", "description": "test menu description"}


def test_create_menu():
    response = client.post('/api/v1/menus', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.json()
    assert 'title' in response.json()
    assert 'description' in response.json()
    assert response.json()['title'] == 'test menu'
    assert response.json()['description'] == 'test menu description'


def test_create_menu_fail():
    response = client.post('/api/v1/menus', json=request_data)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_menus():
    response = client.get('/api/v1/menus')
    assert response.status_code == status.HTTP_200_OK


def test_get_menu_by_id():
    menu_id = "test_menu_id"
    title = "Test Menu"
    description = "This is a test menu"
    gd = get_db()
    db = next(gd)
    menu = Menu(id=menu_id, title=title, description=description)
    db.add(menu)
    db.commit()
    response = client.get(f'/api/v1/menus/{menu_id}')
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == menu_id
    assert data["title"] == title
    assert data["description"] == description
#
#
# def test_update_menu():
#     pass
#
#
# def test_delete_menu():
#     pass
