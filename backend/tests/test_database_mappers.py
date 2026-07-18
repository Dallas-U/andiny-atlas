from datetime import UTC, datetime, timedelta, timezone

from app.core.constants import InvestigationStatus
from app.database.mappers import (
    case_to_investigation,
    investigation_to_case,
    investigation_to_record,
    record_to_investigation,
)
from app.database.models import Investigation
from app.domain import (
    Case,
    Customer,
    InvestigationResult,
)


def test_investigation_to_case_returns_domain_case():
    """An ORM investigation should map into a typed domain case."""

    investigation = Investigation(
        case_id="case-001",
        timestamp=datetime(
            2026,
            7,
            17,
            10,
            30,
        ),
        customer_name="John Doe",
        phone_number="08021234567",
        created_by="user-001",
        status=InvestigationStatus.RESOLVED.value,
        reason="The issue was resolved.",
        next_action="Close the investigation.",
    )

    case = investigation_to_case(investigation)

    assert isinstance(case, Case)
    assert case.case_id == "case-001"
    assert case.timestamp == datetime(
        2026,
        7,
        17,
        10,
        30,
        tzinfo=UTC,
    )
    assert case.customer == Customer(
        name="John Doe",
        phone_number="08021234567",
    )
    assert case.created_by == "user-001"
    assert case.result == InvestigationResult(
        status=InvestigationStatus.RESOLVED,
        reason="The issue was resolved.",
        next_action="Close the investigation.",
    )


def test_investigation_to_case_preserves_aware_timestamp():
    """An existing timezone-aware timestamp should remain unchanged."""

    lagos_timezone = timezone(
        timedelta(hours=1),
    )

    timestamp = datetime(
        2026,
        7,
        17,
        10,
        30,
        tzinfo=lagos_timezone,
    )

    investigation = Investigation(
        case_id="case-001",
        timestamp=timestamp,
        customer_name="John Doe",
        phone_number="08021234567",
        created_by="user-001",
        status=InvestigationStatus.WAITING.value,
        reason="Waiting for customer confirmation.",
        next_action="Contact the customer.",
    )

    case = investigation_to_case(investigation)

    assert case.timestamp == timestamp
    assert case.timestamp.tzinfo is lagos_timezone


def test_case_to_investigation_returns_orm_model():
    """A domain case should map into an ORM investigation."""

    timestamp = datetime(
        2026,
        7,
        17,
        10,
        30,
        tzinfo=UTC,
    )

    case = Case(
        case_id="case-001",
        timestamp=timestamp,
        customer=Customer(
            name="John Doe",
            phone_number="08021234567",
        ),
        created_by="user-001",
        result=InvestigationResult(
            status=InvestigationStatus.ESCALATED,
            reason="Further investigation is required.",
            next_action="Escalate the issue to engineering.",
        ),
    )

    investigation = case_to_investigation(case)

    assert isinstance(investigation, Investigation)
    assert investigation.case_id == "case-001"
    assert investigation.timestamp == timestamp
    assert investigation.customer_name == "John Doe"
    assert investigation.phone_number == "08021234567"
    assert investigation.created_by == "user-001"
    assert investigation.status == InvestigationStatus.ESCALATED.value
    assert investigation.reason == "Further investigation is required."
    assert investigation.next_action == "Escalate the issue to engineering."


def test_legacy_dictionary_mappers_remain_compatible():
    """Legacy dictionary mapping should remain available during migration."""

    record = {
        "case_id": "case-001",
        "timestamp": datetime(
            2026,
            7,
            17,
            10,
            30,
            tzinfo=UTC,
        ).isoformat(),
        "customer_name": "John Doe",
        "phone_number": "08021234567",
        "created_by": "user-001",
        "result": {
            "status": InvestigationStatus.RESOLVED,
            "reason": "The issue was resolved.",
            "next_action": "Close the investigation.",
        },
    }

    investigation = record_to_investigation(record)
    restored_record = investigation_to_record(
        investigation,
    )

    assert restored_record["case_id"] == record["case_id"]
    assert restored_record["timestamp"] == record["timestamp"]
    assert restored_record["customer_name"] == record["customer_name"]
    assert restored_record["phone_number"] == record["phone_number"]
    assert restored_record["created_by"] == record["created_by"]
    assert restored_record["result"]["status"] == InvestigationStatus.RESOLVED.value
    assert restored_record["result"]["reason"] == record["result"]["reason"]
    assert restored_record["result"]["next_action"] == record["result"]["next_action"]
