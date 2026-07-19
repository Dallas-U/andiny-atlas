from datetime import datetime

from pydantic import BaseModel

from app.core.constants import InvestigationStatus


class CaseHistoryResponse(BaseModel):
    """Represents one immutable investigation audit entry."""

    id: str
    case_id: str
    status: InvestigationStatus
    reason: str
    next_action: str
    changed_by: str
    changed_at: datetime