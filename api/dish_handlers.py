from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from db.models import Dish, Menu, SubMenu
from db.session import get_session

from .schemas import DishCreateRequest, DishCreateResponse, DishPatchRequest

dish_router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes'
)


@dish_router.post(
    '/',
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
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='the data are not valid'
        )
    submenu_result = await session.execute(
        select(SubMenu).filter_by(id=submenu_id)
    )
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
    session.add(dish)
    await session.commit()
    await session.refresh(dish)
    await session.close()
    return {
        'id': dish.id,
        'title': dish.title,
        'description': dish.description,
        'price': dish.price
    }


@dish_router.get(
    '',
    tags=['Dishes'])
async def get_dishes(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_session)):
    result = []
    menu_result = await session.execute(select(Menu).filter_by(id=menu_id))
    menu = menu_result.scalar_one_or_none()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    submenu_result = await session.execute(
        select(SubMenu).filter_by(
            id=submenu_id,
            menu_id=menu_id
        )
    )
    if not submenu_result.scalar_one_or_none():
        return []
    dishes_result = await session.execute(
        select(Dish).filter_by(submenu_id=submenu_id)
    )
    for dish in dishes_result:
        data = {
            'id': dish[0].id,
            'title': dish[0].title,
            'description': dish[0].description,
            'price': dish[0].price
        }
        result.append(data)
    return result


@dish_router.get(
    '/{dish_id}',
    tags=['Dishes'])
async def get_dish_by_id(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        session: AsyncSession = Depends(get_session)):
    dish_result = await session.execute(select(Dish).filter_by(id=dish_id))
    dish = dish_result.scalar_one_or_none()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )
    menu_result = await session.execute(select(Menu).filter_by(id=menu_id))
    menu = menu_result.scalar_one_or_none()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    submenu_result = await session.execute(
        select(SubMenu).filter_by(id=submenu_id)
    )
    submenu = submenu_result.scalar_one_or_none()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu does not exist'
        )
    return {
        'id': dish.id,
        'title': dish.title,
        'description': dish.description,
        'price': dish.price
    }


@dish_router.patch(
    '/{dish_id}',
    tags=['Dishes'])
async def update_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        request: DishPatchRequest,
        session: AsyncSession = Depends(get_session)):
    dish_result = await session.execute(select(Dish).filter_by(id=dish_id))
    dish = dish_result.scalar_one_or_none()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )
    menu_result = await session.execute(select(Menu).filter_by(id=menu_id))
    menu = menu_result.scalar_one_or_none()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    submenu_result = await session.execute(
        select(SubMenu).filter_by(id=submenu_id)
    )
    submenu = submenu_result.scalar_one_or_none()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu does not exist'
        )
    if request.title:
        dish.title = request.title
    if request.description:
        dish.description = request.description
    if request.price:
        dish.price = str(round(request.price, 2))
    await session.commit()
    await session.refresh(dish)
    return dish


@dish_router.delete(
    '/{dish_id}',
    tags=['Dishes'])
async def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        session: AsyncSession = Depends(get_session)):
    dish_result = await session.execute(select(Dish).filter_by(id=dish_id))
    dish = dish_result.scalar_one_or_none()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )
    menu_result = await session.execute(select(Menu).filter_by(id=menu_id))
    menu = menu_result.scalar_one_or_none()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu does not exist'
        )
    submenu_result = await session.execute(
        select(SubMenu).filter_by(id=submenu_id)
    )
    submenu = submenu_result.scalar_one_or_none()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu does not exist'
        )
    await session.delete(dish)
    await session.commit()
    return {'message': 'dish deleted successfully'}
