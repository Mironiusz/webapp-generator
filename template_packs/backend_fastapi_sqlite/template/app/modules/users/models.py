from sqlalchemy import String, Text, true
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import CreatedAtMixin, IdMixin, UpdatedAtMixin


class User(IdMixin, CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "users"
    __table_args__ = ({"sqlite_autoincrement": True},)

    username: Mapped[str | None] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(64), unique=True)
    pass_hash: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(server_default=true())
