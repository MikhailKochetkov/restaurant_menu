from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status)
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from uuid import uuid4

from db.models import Menu, SubMenu
from db.session import get_db
from .schemas import (
    MenuCreateRequest,
    MenuCreateResponse,
    MenuPatchRequest)
from .helpers import check_menu

menu_router = APIRouter()


@menu_router.post(
    '/api/v1/menus',
    tags=['Menus'],
    response_model=MenuCreateResponse,
    status_code=201)
async def create_menu(
        request: MenuCreateRequest,
        session: Session = Depends(get_db)):
    try:
        menu = Menu(
            id=str(uuid4()),
            title=request.title,
            description=request.description
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='the data are not valid'
        )
    if session.query(Menu).filter_by(title=request.title).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='menu already exists'
        )
    session.add(menu)
    session.commit()
    session.refresh(menu)
    session.close()
    return {
        "id": menu.id,
        "title": menu.title,
        "description": menu.description
    }


@menu_router.get('/api/v1/menus', tags=['Menus'])
async def get_menus(session: Session = Depends(get_db)):
    menus = session.query(Menu).all()
    result = []
    for menu in menus:
        submenu_count = session.query(
            func.count(SubMenu.id)
        ).filter(SubMenu.menu_id == menu.id).scalar()
        dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)
        data = {
            "id": menu.id,
            "title": menu.title,
            "description": menu.description,
            "submenus_count": submenu_count,
            "dishes_count": dishes_count
        }
        result.append(data)
    return result


@menu_router.get('/api/v1/menus/{menu_id}', tags=['Menus'])
async def get_menu_by_id(menu_id: str, session: Session = Depends(get_db)):
    menu = check_menu(session, menu_id)
    return {
        "id": menu.id,
        "title": menu.title,
        "description": menu.description,
        "submenus_count": session.query(
            func.count(SubMenu.id)
        ).filter(SubMenu.menu_id == menu.id).scalar(),
        "dishes_count": sum(
            len(submenu.dishes) for submenu in menu.submenus
        )
    }


@menu_router.patch('/api/v1/menus/{menu_id}', tags=['Menus'])
async def update_menu(
        menu_id: str,
        request: MenuPatchRequest,
        session: Session = Depends(get_db)):
    menu = check_menu(session, menu_id)
    if request.title:
        menu.title = request.title
    if request.description:
        menu.description = request.description
    session.commit()
    session.refresh(menu)
    return menu


@menu_router.delete('/api/v1/menus/{menu_id}', tags=['Menus'])
async def delete_menu(menu_id: str, session: Session = Depends(get_db)):
    menu = check_menu(session, menu_id)
    session.delete(menu)
    session.commit()
    return {"message": "menu deleted successfully"}
