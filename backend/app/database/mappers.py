from datetime import UTC, datetime

from app.core.constants import InvestigationStatus
from app.database.models import Investigation
from app.domain import Case, Customer
from app.domain import InvestigationResult as DomainInvestigationResult


def _ensure_timezone(
    timestamp: datetime,
) -> datetime:
    """Ensure a datetime has timezone information."""

    if timestamp.tzinfo is None:
        return timestamp.replace(tzinfo=UTC)

    return timestamp


def _to_investigation_status(
    status: InvestigationStatus | str,
) -> InvestigationStatus:
    """Convert a persisted or domain status into an enum value."""

    if isinstance(status, InvestigationStatus):
        return status

    return InvestigationStatus(status)


def investigation_to_case(
    investigation: Investigation,
) -> Case:
    """Convert an ORM investigation into a domain case."""

    return Case(
        case_id=investigation.case_id,
        timestamp=_ensure_timezone(
            investigation.timestamp,
        ),
        customer=Customer(
            name=investigation.customer_name,
            phone_number=investigation.phone_number,
        ),
        created_by=investigation.created_by,
        result=DomainInvestigationResult(
            status=_to_investigation_status(
                investigation.status,
            ),
            reason=investigation.reason,
            next_action=investigation.next_action,
        ),
    )


def case_to_investigation(
    case: Case,
) -> Investigation:
    """Convert a domain case into an ORM investigation."""

    return Investigation(
        case_id=case.case_id,
        timestamp=case.timestamp,
        customer_name=case.customer.name,
        phone_number=case.customer.phone_number,
        created_by=case.created_by,
        status=case.result.status.value,
        reason=case.result.reason,
        next_action=case.result.next_action,
    )
