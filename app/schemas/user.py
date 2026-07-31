"""Pydantic schemas for user registration, login, and serialization."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Validate data used to register a user."""

    username: str = Field(
        min_length=3,
        max_length=50,
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserLogin(BaseModel):
    """Validate user login credentials."""

    username: str = Field(
        min_length=3,
        max_length=50,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserRead(BaseModel):
    """Serialize a user without exposing the password hash."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr


class TokenData(BaseModel):
    """Represent information stored inside a JWT."""

    username: str | None = None


class LoginResponse(BaseModel):
    """Return a successful login response with a JWT."""

    message: str
    access_token: str
    token_type: str
    user: UserRead