from typing import Any

from pydantic import BaseModel, Field

from app.models.workflow import WorkflowDefinition


class SupportCase(BaseModel):
    """Input for a tenant-scoped investigation.

    Generic workflow fields are authoritative. The legacy boolean fields remain
    optional only as a compatibility input during the controlled migration.
    """

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

    workflow_definition_id: str | None = Field(
        default=None,
        description="Selected workflow definition identifier",
    )

    workflow_definition: WorkflowDefinition | None = Field(
        default=None,
        description="Domain-neutral workflow definition for this investigation",
    )

    checks: dict[str, bool] = Field(
        default_factory=dict,
        description="Generic workflow check values keyed by workflow check key",
    )

    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Non-authoritative workflow execution context",
    )

    # Temporary compatibility fields. New core execution must not depend on them.
    payment_verified: bool | None = None
    extension_triggered: bool | None = None
    api_success: bool | None = None
    skg_success: bool | None = None
    device_online: bool | None = None
    sim_slot_one: bool | None = None
    mobile_data_on: bool | None = None

    # Presentation-only demo metadata retained temporarily for compatibility.
    demo_scenario: str | None = Field(
        default=None,
        description="Synthetic demonstration metadata; never drives core workflow execution.",
    )

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
