from pydantic import BaseModel


class MenuCreateRequest(BaseModel):
    title: str
    description: str


class MenuCreateResponse(BaseModel):
    id: str
    title: str
    description: str


class SubMenuCreateRequest(BaseModel):
    title: str
    description: str


class SubMenuCreateResponse(BaseModel):
    id: str
    title: str
    description: str


class DishCreateRequest(BaseModel):
    title: str
    description: str
    price: float


class DishCreateResponse(BaseModel):
    id: str
    title: str
    description: str
    price: str


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
