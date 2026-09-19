from __future__ import annotations

from app.exceptions import ConflictError, NotFoundError


class UserNotFoundError(NotFoundError):
    """Błąd informujący, że użytkownik nie istnieje"""

    detail = "User not found"


class UserAlreadyExistsError(ConflictError):
    """Błąd informujący, że taki użytkownik już istnieje"""

    detail = "User already exists"
