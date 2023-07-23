from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Menu, SubMenu, Dish
from .db_connection import CONNECTION_STRING, PG_CONNECTION_STRING
from settings import DEV_MODE


if DEV_MODE:
    engine = create_engine(CONNECTION_STRING, connect_args={"check_same_thread": False})
    Menu.metadata.create_all(engine)
    SubMenu.metadata.create_all(engine)
    Dish.metadata.create_all(engine)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
else:
    engine = create_engine(PG_CONNECTION_STRING)
    Menu.metadata.create_all(engine)
    SubMenu.metadata.create_all(engine)
    Dish.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
