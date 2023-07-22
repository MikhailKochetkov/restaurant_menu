from pydantic import BaseModel


class MenuCreateRequest(BaseModel):
    title: str
    description: str


class MenuCreateResponse(BaseModel):
    title: str
    description: str


class SubMenuCreateRequest(BaseModel):
    title: str
    description: str
    menu_id: int


class SubMenuCreateResponse(BaseModel):
    id: int
    title: str
    description: str


class DishCreateRequest(BaseModel):
    title: str
    description: str
    price: float
    menu_id: int
    submenu_id: int


class DishCreateResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float


class MenuPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None


class SubMenuPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None


class DishPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
