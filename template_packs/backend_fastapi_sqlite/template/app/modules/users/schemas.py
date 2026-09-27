from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str | None
    email: str
    is_active: bool


class UserCreate(BaseModel):
    username: Annotated[str | None, Field(min_length=3, max_length=64)] = None
    email: Annotated[EmailStr, Field(max_length=254)]
    password: Annotated[str, Field(min_length=8, max_length=128)]


class UserLogin(BaseModel):
    email: Annotated[EmailStr, Field(max_length=254)]
    password: Annotated[str, Field(min_length=8, max_length=128)]


class UserTokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
