from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select

from db.models import Dish, Menu, SubMenu
from db.session import get_session

from .schemas import MenuCreateRequest, MenuCreateResponse, MenuPatchRequest

menu_router = APIRouter(prefix='/api/v1/menus')


@menu_router.post(
    '/',
    tags=['Menus'],
    response_model=MenuCreateResponse,
    status_code=201)
async def create_menu(
        request: MenuCreateRequest,
        session: AsyncSession = Depends(get_session)):
    try:
        menu = Menu(
            id=str(uuid4()),
            title=request.title,
            description=request.description
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='the data are not valid'
        )
    result = await session.execute(select(Menu).filter_by(title=request.title))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='menu already exists'
        )
    session.add(menu)
    await session.commit()
    await session.refresh(menu)
    await session.close()
    return {
        'id': menu.id,
        'title': menu.title,
        'description': menu.description
    }


@menu_router.get('/', tags=['Menus'])
async def get_menus(session: AsyncSession = Depends(get_session)):
    sub_query = select(
        SubMenu.menu_id,
        func.count(Dish.id).label('total_dishes')
    ).join(
        Dish, Dish.submenu_id == SubMenu.id
    ).group_by(SubMenu.menu_id).subquery()
    query = await session.execute(
        select(
            Menu,
            func.coalesce(func.count(SubMenu.id), 0),
            func.coalesce(sub_query.c.total_dishes, 0)
        )
        .outerjoin(SubMenu, SubMenu.menu_id == Menu.id)
        .outerjoin(sub_query, Menu.id == sub_query.c.menu_id)
        .group_by(Menu.id, sub_query.c.total_dishes))
    result = query.all()
    return [{
        'id': q[0].id,
        'title': q[0].title,
        'description': q[0].description,
        'submenus_count': q[1],
        'dishes_count': q[2]
    } for q in result]


@menu_router.get('/{menu_id}', tags=['Menus'])
async def get_menu_by_id(
        menu_id: str,
        session: AsyncSession = Depends(get_session)):
    sub_query = select(
        SubMenu.menu_id,
        func.count(Dish.id).label('total_dishes')
    ).join(Dish, Dish.submenu_id == SubMenu.id).group_by(
        SubMenu.menu_id).subquery()
    query = await session.execute(
        select(
            Menu,
            func.coalesce(func.count(SubMenu.id), 0),
            func.coalesce(sub_query.c.total_dishes, 0)
        ).filter_by(id=menu_id).outerjoin(
            SubMenu, SubMenu.menu_id == Menu.id
        ).outerjoin(
            sub_query, Menu.id == sub_query.c.menu_id
        ).group_by(Menu.id, sub_query.c.total_dishes)
    )
    result = query.first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )
    return {
        'id': result[0].id,
        'title': result[0].title,
        'description': result[0].description,
        'submenus_count': result[1],
        'dishes_count': result[2]
    }


@menu_router.patch('/{menu_id}', tags=['Menus'])
async def update_menu(
        menu_id: str,
        request: MenuPatchRequest,
        session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Menu).filter_by(id=menu_id))
    menu = result.scalar_one_or_none()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )
    if request.title:
        menu.title = request.title
    if request.description:
        menu.description = request.description
    await session.commit()
    await session.refresh(menu)
    return menu


@menu_router.delete('/api/v1/menus/{menu_id}', tags=['Menus'])
async def delete_menu(
        menu_id: str,
        session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Menu).filter_by(id=menu_id))
    menu = result.scalar_one_or_none()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )
    await session.delete(menu)
    await session.commit()
    return {'message': 'menu deleted successfully'}
