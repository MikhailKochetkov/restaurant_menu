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
from .schemas import SubMenuCreateRequest, SubMenuCreateResponse, SubMenuPatchRequest

submenu_router = APIRouter()


@submenu_router.post(
    '/api/v1/menus/{menu_id}/submenus',
    tags=['Create submenu'],
    response_model=SubMenuCreateResponse,
    status_code=201)
async def create_submenu(
        request: SubMenuCreateRequest,
        session: Session = Depends(get_db)):
    try:
        submenu = SubMenu(
            title=request.title,
            description=request.description,
            menu_id=request.menu_id)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The data are not valid.'
        )
    if not session.query(Menu).filter_by(id=request.menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Menu does not exist.'
        )
    if session.query(SubMenu).filter_by(menu_id=request.menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Submenu already exists.'
        )
    session.add(submenu)
    session.commit()
    session.refresh(submenu)
    session.close()
    return {"id": submenu.id, "title": submenu.title, "description": submenu.description}


@submenu_router.get('/api/v1/menus/{menu_id}/submenus', tags=['Get submenus'])
async def get_submenus(menu_id: int, session: Session = Depends(get_db)):
    submenus = session.query(SubMenu).filter_by(menu_id=menu_id).all()
    if not submenus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submenus not found."
        )
    result = []
    for submenu in submenus:
        dishes_count = session.query(func.count(Dish.id)).filter(Dish.submenu_id == submenu.id).scalar()
        data = {
            "id": submenu.id,
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": dishes_count
        }
        result.append(data)
    return result


@submenu_router.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['Get submenu by id'])
async def get_submenu_by_id(menu_id: int, submenu_id: int, session: Session = Depends(get_db)):
    submenu = session.query(SubMenu).filter_by(menu_id=menu_id, id=submenu_id).first()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submenu not found."
        )
    return {"title": submenu.title,
            "description": submenu.description
            }


@submenu_router.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['Update submenu'])
async def update_submenu(
        menu_id: int,
        submenu_id: int,
        request: SubMenuPatchRequest,
        session: Session = Depends(get_db)):
    submenu = session.query(SubMenu).filter_by(id=submenu_id).first()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Submenu not found.'
        )
    if not session.query(Menu).filter_by(id=menu_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Menu does not exist.'
        )
    if request.title:
        submenu.title = request.title
    if request.description:
        submenu.description = request.description
    session.commit()
    session.refresh(submenu)
    return submenu


@submenu_router.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}', tags=['Delete submenu'])
async def delete_submenu(menu_id: int, submenu_id: int, session: Session = Depends(get_db)):
    submenu = session.query(SubMenu).filter_by(id=submenu_id, menu_id=menu_id).first()
    if not submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Submenu not found.'
        )
    session.delete(submenu)
    session.commit()
    return {"message": "Menu deleted successfully"}
