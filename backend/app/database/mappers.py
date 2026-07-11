from datetime import UTC, datetime

from app.core.constants import InvestigationStatus
from app.core.types import CaseRecord
from app.database.models import Investigation


def investigation_to_record(
    investigation: Investigation,
) -> CaseRecord:
    """Convert an ORM investigation into the service-layer structure."""

    timestamp = investigation.timestamp

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=UTC)

    return {
        "case_id": investigation.case_id,
        "timestamp": timestamp.isoformat(),
        "customer_name": investigation.customer_name,
        "phone_number": investigation.phone_number,
        "result": {
            "status": investigation.status,
            "reason": investigation.reason,
            "next_action": investigation.next_action,
        },
    }


def record_to_investigation(
    case: CaseRecord,
) -> Investigation:
    """Convert a service-layer investigation into an ORM model."""

    result = case["result"]
    status = result["status"]

    if isinstance(status, InvestigationStatus):
        status = status.value

    return Investigation(
        case_id=case["case_id"],
        timestamp=datetime.fromisoformat(case["timestamp"]),
        customer_name=case["customer_name"],
        phone_number=case["phone_number"],
        status=status,
        reason=result["reason"],
        next_action=result["next_action"],
    )
