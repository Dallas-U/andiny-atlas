from datetime import UTC, datetime

from app.core.constants import InvestigationStatus
from app.core.types import CaseRecord
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


def investigation_to_record(
    investigation: Investigation,
) -> CaseRecord:
    """Convert an ORM investigation into the legacy service structure."""

    timestamp = _ensure_timezone(
        investigation.timestamp,
    )

    return {
        "case_id": investigation.case_id,
        "timestamp": timestamp.isoformat(),
        "customer_name": investigation.customer_name,
        "phone_number": investigation.phone_number,
        "created_by": investigation.created_by,
        "result": {
            "status": investigation.status,
            "reason": investigation.reason,
            "next_action": investigation.next_action,
        },
    }


def record_to_investigation(
    case: CaseRecord,
) -> Investigation:
    """Convert a legacy service structure into an ORM investigation."""

    result = case["result"]
    status = result["status"]

    if isinstance(status, InvestigationStatus):
        status = status.value

    return Investigation(
        case_id=case["case_id"],
        timestamp=datetime.fromisoformat(
            case["timestamp"],
        ),
        customer_name=case["customer_name"],
        phone_number=case["phone_number"],
        created_by=case["created_by"],
        status=status,
        reason=result["reason"],
        next_action=result["next_action"],
    )
