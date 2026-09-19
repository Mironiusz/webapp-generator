from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str | None
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UsersRead(BaseModel):
    users: list[UserRead]


class UserCreate(BaseModel):
    username: str
    email: str
    pass_plain: str


class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: str
