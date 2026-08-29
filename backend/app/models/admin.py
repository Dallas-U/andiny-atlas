from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.constants import UserRole


class CreateAdminUserRequest(BaseModel):
    """Request used by administrators to provision a user."""

    full_name: str = Field(
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    role: UserRole = UserRole.AGENT

    # Used only when a Super Admin provisions a customer user.
    #
    # Customer Admins must NOT be allowed to use this value to
    # establish their own tenant scope.
    organization_id: str | None = None


class ChangeUserRoleRequest(BaseModel):
    """Request used to change a user's authorization role."""

    role: UserRole


class AdminUserResponse(BaseModel):
    """Public representation of a user in the administration API."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str
    full_name: str
    email: EmailStr
    role: UserRole
    organization_id: str | None
    is_active: bool
    created_at: datetime


class AdminUserListResponse(BaseModel):
    """Paginated collection of users."""

    users: list[AdminUserResponse]

    page: int = Field(
        ge=1,
    )

    page_size: int = Field(
        ge=1,
    )

    total: int = Field(
        ge=0,
    )

    total_pages: int = Field(
        ge=0,
    )