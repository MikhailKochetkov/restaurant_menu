from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status)
from pydantic import ValidationError
from sqlalchemy.orm import Session

from db.models import Dish, Menu, SubMenu
from db.session import get_db
from .schemas import DishCreateRequest, DishCreateResponse, DishPatchRequest

dish_router = APIRouter()


@dish_router.post(
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=DishCreateResponse,
    tags=['Create dish'])
async def create_dish(
        request: DishCreateRequest,
        session: Session = Depends(get_db)):
    try:
        dish = Dish(
            title=request.title,
            description=request.description,
            price=request.price,
            submenu_id=request.submenu_id)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The data are not valid.'
        )
    if not session.query(SubMenu).filter_by(id=request.submenu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Submenu does not exist.'
        )
    if not session.query(Menu).filter_by(id=request.menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Menu does not exist.'
        )
    if session.query(Dish).filter_by(submenu_id=request.submenu_id).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Dish already exists.'
        )
    session.add(dish)
    session.commit()
    session.refresh(dish)
    session.close()
    return {
        "id": dish.id,
        "title": dish.title,
        "description": dish.description,
        "price": round(dish.price, 2)}


@dish_router.get('api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Get dishes'])
async def get_dishes(menu_id: int, submenu_id: int, session: Session = Depends(get_db)):
    dishes = session.query(Dish).filter_by(submenu_id=submenu_id).all()
    if not dishes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dishes not found."
        )
    if not session.query(Menu).filter_by(id=menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Menu does not exist.'
        )
    if not session.query(SubMenu).filter_by(id=submenu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Submenu does not exist.'
        )
    result = []
    for dish in dishes:
        data = {
            "id": dish.id,
            "title": dish.title,
            "description": dish.description,
            "price": round(dish.price, 2)
        }
        result.append(data)
    return result


@dish_router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', tags=['Get dish by id'])
async def get_dish_by_id(menu_id: int, submenu_id: int, dish_id: int, session: Session = Depends(get_db)):
    dish = session.query(Dish).filter_by(id=dish_id).first()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dish not found."
        )
    if not session.query(Menu).filter_by(id=menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Menu does not exist.'
        )
    if not session.query(SubMenu).filter_by(id=submenu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Submenu does not exist.'
        )
    return {"id": dish.id,
            "title": dish.title,
            "description": dish.description,
            "price": round(dish.price, 2)
            }


@dish_router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', tags=['Update dish'])
async def update_dish(
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        request: DishPatchRequest,
        session: Session = Depends(get_db)):
    dish = session.query(Dish).filter_by(id=dish_id).first()
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dish not found.'
        )
    if not session.query(Menu).filter_by(id=menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Menu does not exist.'
        )
    if not session.query(SubMenu).filter_by(id=submenu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Submenu does not exist.'
        )
    if request.title:
        dish.title = request.title
    if request.description:
        dish.description = request.description
    if request.price:
        dish.price = request.price
    session.commit()
    session.refresh(dish)
    return dish


@dish_router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', tags=['Delete dish'])
async def delete_dish(
        menu_id: int,
        submenu_id: int,
        dish_id: int,
        session: Session = Depends(get_db)):
    dish = session.query(Dish).filter_by(id=dish_id).first()
    if not session.query(Menu).filter_by(id=menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Menu does not exist.'
        )
    if not session.query(SubMenu).filter_by(id=submenu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Submenu does not exist.'
        )
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Dish not found.'
        )
    session.delete(dish)
    session.commit()
    return {"message": "Dish deleted successfully"}
