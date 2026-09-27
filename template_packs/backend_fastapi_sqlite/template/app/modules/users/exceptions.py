from __future__ import annotations

from app.exceptions import ConflictError, ForbiddenError, UnauthorizedError


class UserAlreadyExistsError(ConflictError):
    """Błąd informujący, że taki użytkownik już istnieje"""

    detail = "User already exists"


class InvalidCredentialsError(UnauthorizedError):
    """Błąd informujący o błędnych danych uwierzytelniających użytkownika"""

    detail = "Invalid credentials"


class NotAuthenticatedError(UnauthorizedError):
    """Błąd informujący o niepowodzeniu autentykacji"""

    detail = "Not authenticated"


class InactiveUserError(ForbiddenError):
    """Błąd informujący, że użytkownik nie jest aktywny"""

    detail = "Inactive user"
