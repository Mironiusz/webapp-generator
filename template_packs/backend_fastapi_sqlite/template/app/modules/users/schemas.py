from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    id: int
    username: str
    email: str
    pass_plain: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    pass_plain: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
