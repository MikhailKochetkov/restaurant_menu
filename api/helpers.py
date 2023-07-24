from fastapi import HTTPException, status
from db.models import Menu, SubMenu, Dish


def get_first_menu(session, menu_id):
    return session.query(Menu).filter_by(id=menu_id).first()


def get_first_submenu(session, submenu_id):
    return session.query(SubMenu).filter_by(id=submenu_id).first()


def check_menu(session, menu_id):
    menu = get_first_menu(session, menu_id)
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found"
        )
    return menu


def check_submenu_by_menu_id(session, menu_id, submenu_id):
    submenu = session.query(SubMenu).filter_by(
        id=submenu_id,
        menu_id=menu_id
    ).first()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )
    return submenu


def check_dish(session, dish_id):
    dish = session.query(Dish).filter_by(id=dish_id).first()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )
    return dish
