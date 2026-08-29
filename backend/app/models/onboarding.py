from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.constants import UserRole


class CreateCustomerOrganizationRequest(BaseModel):
    """Request used by Super Admin to provision a customer tenant."""

    organization_name: str = Field(
        min_length=2,
        max_length=150,
    )

    organization_code: str = Field(
        min_length=2,
        max_length=50,
    )

    industry: str = Field(
        min_length=2,
        max_length=100,
    )

    contact_email: EmailStr

    admin_full_name: str = Field(
        min_length=2,
        max_length=150,
    )

    admin_email: EmailStr

    admin_password: str = Field(
        min_length=8,
        max_length=128,
    )


class OnboardedOrganizationResponse(BaseModel):
    """Result returned after provisioning a customer tenant."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    organization_id: str
    organization_name: str
    organization_code: str
    industry: str
    contact_email: EmailStr
    organization_is_active: bool

    admin_user_id: str
    admin_full_name: str
    admin_email: EmailStr
    admin_role: UserRole
    admin_organization_id: str
    admin_is_active: bool
    admin_created_at: datetime