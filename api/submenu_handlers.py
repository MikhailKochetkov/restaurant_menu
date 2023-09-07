from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select

from db.models import Dish, Menu, SubMenu
from db.session import get_session

from .schemas import (
    SubMenuCreateRequest,
    SubMenuCreateResponse,
    SubMenuPatchRequest)

submenu_router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus')


@submenu_router.post(
    '/',
    tags=['Submenus'],
    response_model=SubMenuCreateResponse,
    status_code=201)
async def create_submenu(
        menu_id: str,
        request: SubMenuCreateRequest,
        session: AsyncSession = Depends(get_session)):
    try:
        submenu = SubMenu(
            id=uuid4(),
            title=request.title,
            description=request.description,
            menu_id=menu_id)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='the data are not valid'
        )
    menu_result = await session.execute(select(Menu).filter_by(id=menu_id))
    if not menu_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    session.add(submenu)
    await session.commit()
    await session.refresh(submenu)
    await session.close()
    return {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description
    }


@submenu_router.get('/', tags=['Submenus'])
async def get_submenus(
        menu_id: str,
        session: AsyncSession = Depends(get_session)):
    submenus_result = await session.execute(
        select(SubMenu).filter_by(menu_id=menu_id)
    )
    submenus = submenus_result.all()
    result = []
    for submenu in submenus:
        dishes = await session.execute(
            select(
                func.count(Dish.id)
            ).filter(Dish.submenu_id == submenu[0].id))
        dishes_count = dishes.scalar()
        data = {
            'id': submenu[0].id,
            'title': submenu[0].title,
            'description': submenu[0].description,
            'dishes_count': dishes_count
        }
        result.append(data)
    return result


@submenu_router.get(
    '/{submenu_id}',
    tags=['Submenus'])
async def get_submenu_by_id(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_session)):
    submenu_result = await session.execute(select(SubMenu).filter_by(
        id=submenu_id,
        menu_id=menu_id
    ))
    submenu = submenu_result.scalar_one_or_none()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )
    dishes = await session.execute(
        select(
            func.count(Dish.submenu_id)
        ).filter(Dish.submenu_id == submenu.id)
    )
    dishes_count = dishes.scalar()
    return {
        'id': submenu.id,
        'title': submenu.title,
        'description': submenu.description,
        'dishes_count': dishes_count
    }


@submenu_router.patch(
    '/{submenu_id}',
    tags=['Submenus'])
async def update_submenu(
        menu_id: str,
        submenu_id: str,
        request: SubMenuPatchRequest,
        session: AsyncSession = Depends(get_session)):
    submenu_result = await session.execute(
        select(SubMenu).filter_by(id=submenu_id)
    )
    submenu = submenu_result.scalar_one_or_none()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )
    menu_result = await session.execute(select(Menu).filter_by(id=menu_id))
    menu = menu_result.scalar_one_or_none()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    if request.title:
        submenu.title = request.title
    if request.description:
        submenu.description = request.description
    await session.commit()
    await session.refresh(submenu)
    return submenu


@submenu_router.delete(
    '/{submenu_id}',
    tags=['Submenus'])
async def delete_submenu(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_session)):
    submenu_result = await session.execute(
        select(SubMenu)
        .filter_by(id=submenu_id, menu_id=menu_id)
    )
    submenu = submenu_result.scalar_one_or_none()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )
    await session.delete(submenu)
    await session.commit()
    return {'message': 'submenu deleted successfully'}
