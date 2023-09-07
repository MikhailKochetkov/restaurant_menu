from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Menu(Base):
    __tablename__ = 'menus'

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True
    )
    title: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(128))

    submenus = relationship(
        'SubMenu', back_populates='menu', cascade='all, delete'
    )


class SubMenu(Base):
    __tablename__ = 'submenus'

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True
    )
    title: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(128))
    menu_id: Mapped[UUID] = mapped_column(
        ForeignKey('menus.id'), nullable=False
    )

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship(
        'Dish', back_populates='submenu', cascade='all, delete'
    )


class Dish(Base):
    __tablename__ = 'dishes'

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, index=True
    )
    title: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(128))
    price: Mapped[str] = mapped_column(String(64))
    submenu_id: Mapped[UUID] = mapped_column(
        ForeignKey('submenus.id'), nullable=False
    )

    submenu = relationship('SubMenu', back_populates='dishes')
