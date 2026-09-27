from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)
password_hash = PasswordHash.recommended()
settings = get_settings()


class TokenValidationError(Exception):
    """Wyjątek rzucany przy błędzie dekodowania tokenu JWT"""


def hash_password(plain: str) -> str:
    """Funkcja hashująca hasło"""
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Funkcja weryfikująca poprawność podanego hasła"""
    return password_hash.verify(plain, hashed)


def create_access_token(subject: str) -> str:
    """Tworzy podpisany token dostępowy JWT dla podanego `sub`,
    ważny przez `auth.token_lifetime_min` minut od chwili wydania."""
    issued_at = datetime.now(UTC)
    expires_at = issued_at + timedelta(minutes=settings.auth.token_lifetime_min)
    payload = {"sub": subject, "iat": issued_at, "exp": expires_at}

    return jwt.encode(
        payload,
        settings.auth.secret_key.get_secret_value(),
        algorithm=settings.auth.algorithm,
    )


def decode_access_token(token: str) -> str:
    """Dekoduje token JWT: przyjmuje token, a zwraca `sub`
    Weryfikuje token i rzuca TokenValidationError"""
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.auth.secret_key.get_secret_value(),
            algorithms=[settings.auth.algorithm],
            options={"require": ["exp", "iat", "sub"]},
        )
    except jwt.InvalidTokenError as exc:
        logger.info("JWT Token invalid %s", type(exc).__name__)
        raise TokenValidationError from exc

    sub: str = payload["sub"]
    return sub
