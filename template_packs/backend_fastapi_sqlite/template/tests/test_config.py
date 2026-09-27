import pytest
from pydantic import ValidationError

from app.core.config import AuthSettings


@pytest.mark.parametrize("key_length", [32, 64])
def test_auth_settings_accepts_long_enough_key(key_length: int) -> None:
    secret_key = "x" * key_length
    auth_settings = AuthSettings(secret_key=secret_key)
    assert auth_settings.secret_key.get_secret_value() == secret_key


@pytest.mark.parametrize("key_length", [0, 31])
def test_auth_settings_rejects_too_short_key(key_length: int) -> None:
    secret_key = "x" * key_length
    with pytest.raises(ValidationError):
        AuthSettings(secret_key=secret_key)
