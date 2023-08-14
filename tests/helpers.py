import time

from uuid import uuid4
from random import uniform


def create_unique_menu():
    unique_id = str(uuid4())
    timestamp = str(time.time())
    menu = {
        "title": f"test menu title  {unique_id}",
        "description": f"test menu description {timestamp}"
    }
    return menu


def create_unique_submenu(menu_id):
    unique_id = str(uuid4())
    timestamp = str(time.time())
    submenu = {
        "title": f"test submenu title {unique_id}",
        "description": f"test submenu description {timestamp}",
        "menu_id": f"{menu_id}"
    }
    return submenu


def create_unique_dish(submenu_id):
    unique_id = str(uuid4())
    timestamp = str(time.time())
    price = round(uniform(1, 10), 2)
    dish = {
        "title": f"test dish title {unique_id}",
        "description": f"test dish description {timestamp}",
        "price": price,
        "submenu_id": f"{submenu_id}"
    }
    return dish
