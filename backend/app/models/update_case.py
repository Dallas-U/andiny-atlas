from pydantic import BaseModel, Field

from app.core.constants import InvestigationStatus


class UpdateCaseRequest(BaseModel):
    """Editable investigation fields."""

    status: InvestigationStatus = Field(
        description="Updated investigation status.",
    )
    reason: str = Field(
        min_length=1,
        max_length=500,
        description="Updated investigation reason.",
    )
    next_action: str = Field(
        min_length=1,
        max_length=500,
        description="Updated next action.",
    )
