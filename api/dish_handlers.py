from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status)
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select
from uuid import uuid4

from db.models import Dish, SubMenu, Menu
from db.session import get_session
from .schemas import (
    DishCreateRequest,
    DishCreateResponse,
    DishPatchRequest)
from .helpers import (
    check_dish,
    get_first_menu,
    get_first_submenu)

dish_router = APIRouter()


@dish_router.post(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=DishCreateResponse,
    tags=['Dishes'],
    status_code=201)
async def create_dish(
        menu_id: str,
        submenu_id: str,
        request: DishCreateRequest,
        session: AsyncSession = Depends(get_session)):
    try:
        dish = Dish(
            id=str(uuid4()),
            title=request.title,
            description=request.description,
            price=str(round(request.price, 2)),
            submenu_id=submenu_id)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='the data are not valid'
        )
    submenu_result = await session.execute(select(SubMenu).filter_by(id=submenu_id))
    if not submenu_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu does not exist'
        )
    menu_result = await session.execute(select(Menu).filter_by(id=menu_id))
    if not menu_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    dish_result = await session.execute(
        select(Dish)
        .filter_by(
            title=request.title,
            submenu_id=submenu_id
        )
    )
    if dish_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='dish already exists'
        )
    session.add(dish)
    await session.commit()
    await session.refresh(dish)
    await session.close()
    return {
        "id": dish.id,
        "title": dish.title,
        "description": dish.description,
        "price": dish.price
    }


@dish_router.get(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dishes'])
async def get_dishes(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_session)):
    result = []
    if not get_first_menu(session, menu_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    if not session.query(SubMenu).filter_by(
            id=submenu_id,
            menu_id=menu_id).first():
        return []
    dishes = session.query(Dish).filter_by(submenu_id=submenu_id).all()
    for dish in dishes:
        data = {
            "id": dish.id,
            "title": dish.title,
            "description": dish.description,
            "price": dish.price
        }
        result.append(data)
    return result


@dish_router.get(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    tags=['Dishes'])
async def get_dish_by_id(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        session: AsyncSession = Depends(get_session)):
    dish = check_dish(session, dish_id)
    if not get_first_menu(session, menu_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    if not get_first_submenu(session, submenu_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu does not exist'
        )
    return {
        "id": dish.id,
        "title": dish.title,
        "description": dish.description,
        "price": dish.price
    }


@dish_router.patch(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    tags=['Dishes'])
async def update_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        request: DishPatchRequest,
        session: AsyncSession = Depends(get_session)):
    dish = check_dish(session, dish_id)
    if not get_first_menu(session, menu_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    if not get_first_submenu(session, submenu_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu does not exist'
        )
    if request.title:
        dish.title = request.title
    if request.description:
        dish.description = request.description
    if request.price:
        dish.price = request.price
    await session.commit()
    await session.refresh(dish)
    return dish


@dish_router.delete(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    tags=['Dishes'])
async def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        session: AsyncSession = Depends(get_session)):
    dish = check_dish(session, dish_id)
    if not get_first_menu(session, menu_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    if not get_first_submenu(session, submenu_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu does not exist'
        )
    await session.delete(dish)
    await session.commit()
    return {"message": "dish deleted successfully"}
