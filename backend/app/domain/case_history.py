from dataclasses import dataclass
from datetime import datetime

from app.core.constants import InvestigationStatus


@dataclass(frozen=True, slots=True)
class CaseHistory:
    """Represents an immutable investigation history entry."""

    id: int | None
    case_id: str
    status: InvestigationStatus
    reason: str
    next_action: str
    changed_by: str
    changed_at: datetime
