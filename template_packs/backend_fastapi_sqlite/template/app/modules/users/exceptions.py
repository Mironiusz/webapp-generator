from __future__ import annotations

from app.exceptions import ConflictError, ForbiddenError, NotFoundError, UnauthorizedError


class UserNotFoundError(NotFoundError):
    """Błąd informujący, że użytkownik nie istnieje"""

    detail = "User not found"


class UserAlreadyExistsError(ConflictError):
    """Błąd informujący, że taki użytkownik już istnieje"""

    detail = "User already exists"


class InvalidCredentialsError(UnauthorizedError):
    """Błąd informujący o błędnych danych uwierzytelniających użytkownika"""

    detail = "Invalid credentials"


class InactiveUserError(ForbiddenError):
    """Błąd informujący, że użytkownik nie jest zalogowany"""

    detail = "Inactive user"
