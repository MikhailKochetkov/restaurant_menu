from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status)
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select
from uuid import uuid4

from db.models import SubMenu, Dish, Menu
from db.session import get_session
from .schemas import (
    SubMenuCreateRequest,
    SubMenuCreateResponse,
    SubMenuPatchRequest)
from .helpers import (
    check_submenu_by_menu_id)

submenu_router = APIRouter()


@submenu_router.post(
    '/api/v1/menus/{menu_id}/submenus',
    tags=['Submenus'],
    response_model=SubMenuCreateResponse,
    status_code=201)
async def create_submenu(
        menu_id: str,
        request: SubMenuCreateRequest,
        session: AsyncSession = Depends(get_session)):
    try:
        submenu = SubMenu(
            id=str(uuid4()),
            title=request.title,
            description=request.description,
            menu_id=menu_id)
    except ValidationError as e:
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
    submenu_result = await session.execute(select(SubMenu).filter_by(menu_id=menu_id))
    if submenu_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='submenu already exists'
        )
    session.add(submenu)
    await session.commit()
    await session.refresh(submenu)
    await session.close()
    return {
        "id": submenu.id,
        "title": submenu.title,
        "description": submenu.description
    }


@submenu_router.get('/api/v1/menus/{menu_id}/submenus', tags=['Submenus'])
async def get_submenus(menu_id: str, session: AsyncSession = Depends(get_session)):
    # TODO: 3 correct errors
    submenus_result = await session.execute(select(SubMenu).filter_by(menu_id=menu_id))
    result = []
    for submenu in submenus_result:
        dishes = await session.execute(
            select(
                Dish,
                func.count(Dish.id)
            ).filter(Dish.submenu_id == submenu.id))
        dishes_count = dishes.scalar()
        data = {
            "id": submenu.id,
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": dishes_count
        }
        result.append(data)
    return result


@submenu_router.get(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    tags=['Submenus'])
async def get_submenu_by_id(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_session)):
    # TODO: 4 correct errors
    submenu = check_submenu_by_menu_id(session, menu_id, submenu_id)
    dishes_count = session.query(
        func.count(Dish.submenu_id)
    ).filter(Dish.submenu_id == submenu.id).scalar()
    return {
        "id": submenu.id,
        "title": submenu.title,
        "description": submenu.description,
        "dishes_count": dishes_count
    }


@submenu_router.patch(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    tags=['Submenus'])
async def update_submenu(
        menu_id: str,
        submenu_id: str,
        request: SubMenuPatchRequest,
        session: AsyncSession = Depends(get_session)):
    submenu_result = await session.execute(select(SubMenu).filter_by(id=submenu_id))
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
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    tags=['Submenus'])
async def delete_submenu(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_session)):
    submenu_result = await session.execute(
        select(SubMenu)
        .filter_by(
            id=submenu_id,
            menu_id=menu_id
        )
    )
    submenu = submenu_result.scalar_one_or_none()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )
    await session.delete(submenu)
    await session.commit()
    return {"message": "menu deleted successfully"}
