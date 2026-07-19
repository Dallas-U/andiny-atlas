from datetime import UTC, datetime, timedelta, timezone

from app.core.constants import InvestigationStatus
from app.database.mappers import (
    case_to_investigation,
    domain_user_to_orm,
    investigation_to_case,
    orm_user_to_domain,
)
from app.database.models import Investigation, User as ORMUser
from app.domain import (
    Case,
    Customer,
    InvestigationResult,
    User,
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
    lagos_timezone = timezone(timedelta(hours=1))

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


def test_case_mapper_round_trip_preserves_domain_case():
    case = Case(
        case_id="case-001",
        timestamp=datetime(
            2026,
            7,
            17,
            10,
            30,
            tzinfo=UTC,
        ),
        customer=Customer(
            name="John Doe",
            phone_number="08021234567",
        ),
        created_by="user-001",
        result=InvestigationResult(
            status=InvestigationStatus.RESOLVED,
            reason="The issue was resolved.",
            next_action="Close the investigation.",
        ),
    )

    investigation = case_to_investigation(case)
    restored_case = investigation_to_case(investigation)

    assert restored_case == case


def test_orm_user_to_domain_returns_domain_user():
    created_at = datetime(
        2026,
        7,
        18,
        10,
        0,
        tzinfo=UTC,
    )

    orm_user = ORMUser(
        id="user-001",
        full_name="John Doe",
        email="john@example.com",
        hashed_password="hashed-password",
        is_active=True,
        created_at=created_at,
    )

    user = orm_user_to_domain(orm_user)

    assert user == User(
        id="user-001",
        full_name="John Doe",
        email="john@example.com",
        hashed_password="hashed-password",
        is_active=True,
        created_at=created_at,
    )


def test_domain_user_to_orm_returns_sqlalchemy_user():
    created_at = datetime(
        2026,
        7,
        18,
        10,
        0,
        tzinfo=UTC,
    )

    user = User(
        id="user-001",
        full_name="John Doe",
        email="john@example.com",
        hashed_password="hashed-password",
        is_active=True,
        created_at=created_at,
    )

    orm_user = domain_user_to_orm(user)

    assert isinstance(orm_user, ORMUser)
    assert orm_user.id == user.id
    assert orm_user.full_name == user.full_name
    assert orm_user.email == user.email
    assert orm_user.hashed_password == user.hashed_password
    assert orm_user.is_active == user.is_active
    assert orm_user.created_at == user.created_at


def test_user_mapper_round_trip_preserves_domain_user():
    user = User(
        id="user-001",
        full_name="John Doe",
        email="john@example.com",
        hashed_password="hashed-password",
        is_active=True,
        created_at=datetime(
            2026,
            7,
            18,
            10,
            0,
            tzinfo=UTC,
        ),
    )

    orm_user = domain_user_to_orm(user)
    restored_user = orm_user_to_domain(orm_user)

    assert restored_user == user