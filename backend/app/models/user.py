from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Request model for creating a user."""

    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Request model for authenticating a user."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Response model returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    """JWT access token."""

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    sub: str
    exp: int
