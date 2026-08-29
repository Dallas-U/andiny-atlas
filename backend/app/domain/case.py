from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.core.constants import InvestigationStatus


@dataclass(frozen=True, slots=True)
class Customer:
    """
    Customer information associated with a support investigation.
    """

    name: str
    phone_number: str


@dataclass(frozen=True, slots=True)
class InvestigationResult:
    """
    Outcome of an investigation.
    """

    status: InvestigationStatus
    reason: str
    next_action: str


@dataclass(frozen=True, slots=True)
class Case:
    """
    Domain representation of a support investigation.

    Enterprise ownership fields identify the organization, branch,
    and department responsible for the investigation.
    """

    case_id: str
    timestamp: datetime
    customer: Customer
    created_by: str
    result: InvestigationResult

    organization_id: str | None = None
    branch_id: str | None = None
    department_id: str | None = None