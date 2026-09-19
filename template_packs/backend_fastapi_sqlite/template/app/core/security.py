from __future__ import annotations

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(plain: str) -> str:
    """Funkcja hashująca hasło"""
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Funkcja weryfikująca poprawność podanego hasła"""
    return password_hash.verify(plain, hashed)
