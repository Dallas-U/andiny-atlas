from dataclasses import dataclass
from datetime import datetime

from app.core.constants import InvestigationStatus
from app.domain.customer import Customer


@dataclass(frozen=True, slots=True)
class InvestigationResult:
    """Represents the current outcome of an investigation."""

    status: InvestigationStatus
    reason: str
    next_action: str


@dataclass(frozen=True, slots=True)
class Case:
    """Represents an investigation case in the domain layer."""

    case_id: str
    timestamp: datetime
    customer: Customer
    created_by: str
    result: InvestigationResult
