from pydantic import BaseModel

from app.core.constants import InvestigationStatus


class InvestigationResult(BaseModel):
    """Represents the result of a support investigation."""

    status: InvestigationStatus
    reason: str
    next_action: str


class CaseResponse(BaseModel):
    """Represents a stored investigation case."""

    case_id: str
    timestamp: str
    customer_name: str
    phone_number: str
    created_by: str

    organization_id: str | None = None
    branch_id: str | None = None
    department_id: str | None = None

    result: InvestigationResult