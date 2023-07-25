from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status)
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from uuid import uuid4

from db.models import Menu, SubMenu, Dish
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
    sub_query = session.query(
        SubMenu.menu_id,
        func.count(Dish.id).label('total_dishes')
    ).join(
        Dish, Dish.submenu_id == SubMenu.id).group_by(SubMenu.menu_id).subquery()
    query = session.query(
        Menu,
        func.coalesce(func.count(SubMenu.id), 0),
        func.coalesce(sub_query.c.total_dishes, 0)
    ).outerjoin(SubMenu, SubMenu.menu_id == Menu.id).outerjoin(
        sub_query, Menu.id == sub_query.c.menu_id
    ).group_by(Menu.id).all()
    result = [{
        "id": q[0].id,
        "title": q[0].title,
        "description": q[0].description,
        "submenus_count": q[1],
        "dishes_count": q[2]

    } for q in query]
    return result


@menu_router.get('/api/v1/menus/{menu_id}', tags=['Menus'])
async def get_menu_by_id(menu_id: str, session: Session = Depends(get_db)):
    sub_query = session.query(
        SubMenu.menu_id,
        func.count(Dish.id).label('total_dishes')
    ).join(Dish, Dish.submenu_id == SubMenu.id).group_by(
        SubMenu.menu_id).subquery()
    query = session.query(
        Menu,
        func.coalesce(func.count(SubMenu.id), 0),
        func.coalesce(sub_query.c.total_dishes, 0)
    ).filter_by(id=menu_id).outerjoin(
        SubMenu, SubMenu.menu_id == Menu.id
    ).outerjoin(
        sub_query, Menu.id == sub_query.c.menu_id
    ).group_by(Menu.id).first()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found"
        )
    return {
        "id": query[0].id,
        "title": query[0].title,
        "description": query[0].description,
        "submenus_count": query[1],
        "dishes_count": query[2]
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
