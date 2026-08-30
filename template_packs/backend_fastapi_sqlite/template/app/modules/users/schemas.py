from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    pass_plain: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UsersRead(BaseModel):
    users: list[UserRead]
