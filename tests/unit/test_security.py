"""Unit tests for password and JWT security utilities."""

import pytest

from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_does_not_store_plain_text() -> None:
    """A password should be converted to a secure hash."""

    password = "SecurePass123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True


def test_verify_password_rejects_wrong_password() -> None:
    """An incorrect password should not match the stored hash."""

    hashed = hash_password("SecurePass123!")

    assert verify_password("WrongPassword123!", hashed) is False


def test_create_and_decode_access_token() -> None:
    """A generated token should preserve its subject."""

    token = create_access_token(subject="testuser")
    payload = decode_access_token(token)

    assert payload["sub"] == "testuser"
    assert "exp" in payload


def test_decode_access_token_rejects_invalid_token() -> None:
    """An invalid JWT should raise a clear error."""

    with pytest.raises(
        ValueError,
        match="Invalid or expired access token",
    ):
        decode_access_token("not-a-valid-token")
