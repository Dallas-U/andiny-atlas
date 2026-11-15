
from datetime import UTC, date, datetime
from types import SimpleNamespace
from uuid import uuid4

import pytest
from sqlalchemy.dialects import postgresql, sqlite

from app.database.models import Investigation
from app.models.analytics import AnalyticsInterval
from app.repositories.analytics_repository import AnalyticsRepository


def make_investigation(timestamp, organization_id=None):
    return Investigation(
        case_id=str(uuid4()),
        timestamp=timestamp,
        customer_name="Analytics Test Customer",
        phone_number="08012345678",
        created_by="analytics-test-user",
        organization_id=organization_id,
        branch_id=None,
        department_id=None,
        status="resolved",
        reason="Analytics repository test",
        next_action="Complete analytics validation",
    )


@pytest.mark.parametrize(
    ("interval", "expected"),
    [
        (AnalyticsInterval.DAY, [("2026-10-01", 1), ("2026-10-02", 1)]),
        (AnalyticsInterval.WEEK, [("2026-W39", 2)]),
        (AnalyticsInterval.MONTH, [("2026-10", 2)]),
    ],
)
def test_get_trend_groups_sqlite_records(
    test_session_factory,
    interval,
    expected,
):
    with test_session_factory() as session:
        session.add_all(
            [
                make_investigation(
                    datetime(2026, 10, 1, 10, 0, tzinfo=UTC)
                ),
                make_investigation(
                    datetime(2026, 10, 2, 10, 0, tzinfo=UTC)
                ),
            ]
        )
        session.commit()

    repository = AnalyticsRepository(
        session_factory=test_session_factory
    )

    result = repository.get_trend(
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 2),
        interval=interval,
    )

    assert result == expected


def test_get_trend_sqlite_week_zero_and_year_boundary(
    test_session_factory,
):
    with test_session_factory() as session:
        session.add_all(
            [
                make_investigation(
                    datetime(2026, 12, 31, 12, 0, tzinfo=UTC)
                ),
                make_investigation(
                    datetime(2027, 1, 1, 12, 0, tzinfo=UTC)
                ),
                make_investigation(
                    datetime(2027, 1, 4, 12, 0, tzinfo=UTC)
                ),
            ]
        )
        session.commit()

    repository = AnalyticsRepository(
        session_factory=test_session_factory
    )

    result = repository.get_trend(
        start_date=date(2026, 12, 31),
        end_date=date(2027, 1, 4),
        interval=AnalyticsInterval.WEEK,
    )

    assert result == [
        ("2026-W52", 1),
        ("2027-W00", 1),
        ("2027-W01", 1),
    ]


@pytest.mark.parametrize(
    "interval",
    [
        AnalyticsInterval.DAY,
        AnalyticsInterval.WEEK,
        AnalyticsInterval.MONTH,
    ],
)
def test_postgresql_trend_expression_uses_utc(interval):
    expression = AnalyticsRepository._trend_period_expression(
        interval,
        "postgresql",
    )

    compiled_expression = expression.compile(
        dialect=postgresql.dialect(),
    )
    compiled = str(compiled_expression)

    assert "timezone(" in compiled
    assert "investigations.timestamp" in compiled
    assert "UTC" in compiled_expression.params.values()
    assert "to_char" in compiled

    if interval == AnalyticsInterval.WEEK:
        assert "make_date" in compiled
        assert "isodow" in compiled
        assert "doy" in compiled


def test_sqlite_trend_expression_preserves_strftime():
    expression = AnalyticsRepository._trend_period_expression(
        AnalyticsInterval.DAY,
        "sqlite",
    )

    compiled = str(
        expression.compile(
            dialect=sqlite.dialect(),
        )
    )

    assert "strftime" in compiled
    assert "investigations.timestamp" in compiled


def test_get_trend_rejects_unsupported_database_dialect():
    with pytest.raises(
        NotImplementedError,
        match="not supported",
    ):
        AnalyticsRepository._trend_period_expression(
            AnalyticsInterval.DAY,
            "unsupported",
        )


def test_get_trend_applies_organization_filter():
    class FakeResult:
        def all(self):
            return []

    class FakeSession:
        def __init__(self):
            self.statement = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

        def get_bind(self):
            return SimpleNamespace(
                dialect=SimpleNamespace(name="sqlite")
            )

        def execute(self, statement):
            self.statement = statement
            return FakeResult()

    fake_session = FakeSession()

    repository = AnalyticsRepository(
        session_factory=lambda: fake_session
    )

    repository.get_trend(
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 31),
        interval=AnalyticsInterval.DAY,
        organization_id="test-organization-001",
    )

    compiled = fake_session.statement.compile(
        dialect=sqlite.dialect()
    )

    assert "investigations.organization_id = ?" in str(compiled)
    assert "test-organization-001" in compiled.params.values()
