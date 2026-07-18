from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from app.core.constants import InvestigationStatus
from app.domain import (
    Case,
    CaseHistory,
    Customer,
    InvestigationResult,
)


def test_customer_contains_explicit_domain_fields():
    """A customer should expose its name and phone number."""

    customer = Customer(
        name="John Doe",
        phone_number="08021234567",
    )

    assert customer.name == "John Doe"
    assert customer.phone_number == "08021234567"


def test_customer_is_immutable():
    """A customer value object should not be mutated accidentally."""

    customer = Customer(
        name="John Doe",
        phone_number="08021234567",
    )

    with pytest.raises(FrozenInstanceError):
        customer.name = "Jane Doe"


def test_case_contains_explicit_domain_fields():
    """A case should expose its investigation data through typed fields."""

    timestamp = datetime(
        2026,
        7,
        11,
        10,
        0,
        tzinfo=UTC,
    )

    customer = Customer(
        name="John Doe",
        phone_number="08021234567",
    )

    result = InvestigationResult(
        status=InvestigationStatus.RESOLVED,
        reason="The issue was resolved.",
        next_action="Close the investigation.",
    )

    case = Case(
        case_id="case-001",
        timestamp=timestamp,
        customer=customer,
        created_by="user-001",
        result=result,
    )

    assert case.case_id == "case-001"
    assert case.timestamp == timestamp
    assert case.customer == customer
    assert case.customer.name == "John Doe"
    assert case.customer.phone_number == "08021234567"
    assert case.created_by == "user-001"
    assert case.result == result
    assert case.result.status is InvestigationStatus.RESOLVED


def test_case_is_immutable():
    """A persisted case representation should not be mutated accidentally."""

    case = Case(
        case_id="case-001",
        timestamp=datetime.now(UTC),
        customer=Customer(
            name="John Doe",
            phone_number="08021234567",
        ),
        created_by="user-001",
        result=InvestigationResult(
            status=InvestigationStatus.WAITING,
            reason="Waiting for customer confirmation.",
            next_action="Contact the customer.",
        ),
    )

    with pytest.raises(FrozenInstanceError):
        case.created_by = "user-002"


def test_investigation_result_is_immutable():
    """An investigation result should be replaced rather than mutated."""

    result = InvestigationResult(
        status=InvestigationStatus.WAITING,
        reason="Waiting for customer confirmation.",
        next_action="Contact the customer.",
    )

    with pytest.raises(FrozenInstanceError):
        result.reason = "Changed reason."


def test_case_history_contains_audit_information():
    """A history entry should record what changed, who changed it, and when."""

    changed_at = datetime(
        2026,
        7,
        15,
        12,
        30,
        tzinfo=UTC,
    )

    history = CaseHistory(
        id=1,
        case_id="case-001",
        status=InvestigationStatus.ESCALATED,
        reason="Further technical investigation is required.",
        next_action="Escalate the issue to engineering.",
        changed_by="user-001",
        changed_at=changed_at,
    )

    assert history.id == 1
    assert history.case_id == "case-001"
    assert history.status is InvestigationStatus.ESCALATED
    assert history.reason == ("Further technical investigation is required.")
    assert history.next_action == ("Escalate the issue to engineering.")
    assert history.changed_by == "user-001"
    assert history.changed_at == changed_at


def test_new_case_history_can_exist_without_database_id():
    """A history entry may be created before its ID is generated."""

    history = CaseHistory(
        id=None,
        case_id="case-001",
        status=InvestigationStatus.RESOLVED,
        reason="The customer confirmed successful resolution.",
        next_action="Close the investigation.",
        changed_by="user-001",
        changed_at=datetime.now(UTC),
    )

    assert history.id is None


def test_case_history_is_immutable():
    """Recorded investigation history must not be editable."""

    history = CaseHistory(
        id=1,
        case_id="case-001",
        status=InvestigationStatus.RESOLVED,
        reason="The issue was resolved.",
        next_action="Close the investigation.",
        changed_by="user-001",
        changed_at=datetime.now(UTC),
    )

    with pytest.raises(FrozenInstanceError):
        history.reason = "Modified historical reason."
