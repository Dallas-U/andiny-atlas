from pydantic import BaseModel, Field


class SupportCase(BaseModel):
    customer_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Customer's full name",
    )

    phone_number: str = Field(
        ...,
        min_length=7,
        max_length=20,
        description="Customer phone number",
    )

    country: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Customer country",
    )

    payment_verified: bool
    extension_triggered: bool
    api_success: bool
    skg_success: bool
    device_online: bool
    sim_slot_one: bool
    mobile_data_on: bool

    # Enterprise ownership (optional for backward compatibility)
    organization_id: str | None = Field(
        default=None,
        description="Organization that owns the investigation",
    )

    branch_id: str | None = Field(
        default=None,
        description="Branch that owns the investigation",
    )

    department_id: str | None = Field(
        default=None,
        description="Department that owns the investigation",
    )