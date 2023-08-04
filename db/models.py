from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menus'

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(128))

    submenus = relationship('SubMenu', back_populates='menu', cascade='all, delete')


class SubMenu(Base):
    __tablename__ = 'submenus'

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(128))
    menu_id: Mapped[int] = mapped_column(ForeignKey('menus.id'), nullable=False)

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete')


class Dish(Base):
    __tablename__ = 'dishes'

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(128))
    price: Mapped[str] = mapped_column(String(64))
    submenu_id: Mapped[str] = mapped_column(String, ForeignKey('submenus.id'), nullable=False)

    submenu = relationship('SubMenu', back_populates='dishes')
