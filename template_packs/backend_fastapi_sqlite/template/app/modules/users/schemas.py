from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str | None
    email: str
    is_active: bool


class UsersRead(BaseModel):
    users: list[UserRead]


class UserCreate(BaseModel):
    username: Annotated[str | None, Field(min_length=3, max_length=64)] = None
    email: Annotated[EmailStr, Field(max_length=254)]
    password: Annotated[str, Field(min_length=8, max_length=128)]
