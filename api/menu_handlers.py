from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status)
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from db.models import Menu, SubMenu, Dish
from db.session import get_db
from .schemas import (
    MenuCreateRequest,
    MenuCreateResponse,
    MenuPatchRequest)

menu_router = APIRouter()


@menu_router.post(
    '/api/v1/menus',
    tags=['Create menu'],
    response_model=MenuCreateResponse,
    status_code=201)
async def create_menu(
        request: MenuCreateRequest,
        session: Session = Depends(get_db)):
    try:
        menu = Menu(title=request.title, description=request.description)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The data are not valid.'
        )
    if session.query(Menu).filter_by(title=request.title).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Menu already exists.'
        )
    session.add(menu)
    session.commit()
    session.refresh(menu)
    session.close()
    return {"title": menu.title, "description": menu.description}


@menu_router.get('/api/v1/menus', tags=['Get menus'])
async def get_menus(session: Session = Depends(get_db)):
    menus = session.query(Menu).all()
    if not menus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menus not found."
        )
    result = []
    for menu in menus:
        submenu_count = session.query(func.count(SubMenu.id)).filter(SubMenu.menu_id == menu.id).scalar()
        dishes_count = session.query(func.count(Dish.id)).filter(Dish.submenu_id == SubMenu.id).scalar()
        data = {
            "id": menu.id,
            "title": menu.title,
            "description": menu.description,
            "submenus_count": submenu_count,
            "dishes_count": dishes_count
        }
        result.append(data)
    return result


@menu_router.get('/api/v1/menus/{menu_id}', tags=['Get menu by id'])
async def get_menu_by_id(menu_id: int, session: Session = Depends(get_db)):
    menu = session.query(Menu).filter_by(id=menu_id).first()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found."
        )
    return {"title": menu.title,
            "description": menu.description,
            "submenus_count": session.query(func.count(SubMenu.id)).filter(SubMenu.menu_id == menu.id).scalar(),
            "dishes_count": session.query(func.count(Dish.id)).filter(Dish.submenu_id == SubMenu.id).scalar()
            }


@menu_router.patch('/api/v1/menus/{menu_id}', tags=['Update menu'])
async def update_menu(menu_id: int, request: MenuPatchRequest, session: Session = Depends(get_db)):
    menu = session.query(Menu).filter_by(id=menu_id).first()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Menu not found.'
        )
    if request.title:
        menu.title = request.title
    if request.description:
        menu.description = request.description
    session.commit()
    session.refresh(menu)
    return menu


@menu_router.delete('/api/v1/menus/{menu_id}', tags=['Delete menu'])
async def delete_menu(menu_id: int, session: Session = Depends(get_db)):
    menu = session.query(Menu).filter_by(id=menu_id).first()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Menu not found.'
        )
    session.delete(menu)
    session.commit()
    return {"message": "Menu deleted successfully"}
