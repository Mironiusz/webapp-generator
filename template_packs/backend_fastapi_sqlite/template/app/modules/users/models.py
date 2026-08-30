from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[String | None] = mapped_column(String(64))
    email: Mapped[String] = mapped_column(String(64), unique=True)
    pass_hash: Mapped[String] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    created_at: Mapped[DateTime] = mapped_column()
    updated_at: Mapped[DateTime] = mapped_column()
