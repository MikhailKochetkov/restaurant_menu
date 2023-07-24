from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    submenus = relationship(
        'SubMenu',
        back_populates='menu',
        cascade='all, delete'
    )


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(String, ForeignKey('menus.id'), nullable=False)
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship(
        'Dish',
        back_populates='submenu',
        cascade='all, delete'
    )


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(String, ForeignKey('submenus.id'), nullable=False)
    submenu = relationship('SubMenu', back_populates='dishes')
