from __future__ import annotations

from typing import ClassVar

from fastapi import status


class AppError(Exception):
    """Bazowa klasa błędu"""

    status_code: ClassVar[int]
    detail: ClassVar[str]

    def __init__(self) -> None:
        super().__init__(self.detail)


class NotFoundError(AppError):
    """Bazowa klasa błędu typu `404 Not Found`"""

    status_code = status.HTTP_404_NOT_FOUND


class ConflictError(AppError):
    """Bazowa klasa błędu typu `409 Conflict`"""

    status_code = status.HTTP_409_CONFLICT
