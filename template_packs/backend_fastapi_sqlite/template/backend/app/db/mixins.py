from __future__ import annotations

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    """Dokłada modelowi kolumnę id"""

    id: Mapped[int] = mapped_column(primary_key=True, sort_order=-100)


class CreatedAtMixin:
    """Dokłada modelowi kolumnę created_at"""

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class UpdatedAtMixin:
    """Dokłada modelowi kolumnę updated_at"""

    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
