
from datetime import UTC, date, datetime, time, timedelta

from sqlalchemy import (
    Integer,
    String,
    case,
    cast,
    extract,
    func,
    select,
)

from app.core.constants import InvestigationStatus
from app.database.models import Investigation, Organization, User
from app.database.session import SessionLocal
from app.models.analytics import AnalyticsInterval


class AnalyticsRepository:
    """Read-only repository for tenant-scoped investigation analytics."""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def get_organization_overview(self):
        """
        Return organization-level metrics.

        This method is intentionally platform-level and must only be exposed
        through a Super Admin protected endpoint.
        """

        with self.session_factory() as session:
            rows = session.execute(
                select(
                    Organization.organization_id,
                    Organization.name,
                    Organization.code,
                    Organization.industry,
                    Organization.is_active,
                    func.count(
                        Investigation.case_id
                    ).label("total_cases"),
                    func.sum(
                        Investigation.status
                        == InvestigationStatus.RESOLVED.value
                    ).label("resolved_cases"),
                    func.sum(
                        Investigation.status
                        == InvestigationStatus.ESCALATED.value
                    ).label("escalated_cases"),
                )
                .select_from(Organization)
                .outerjoin(
                    Investigation,
                    Investigation.organization_id
                    == Organization.organization_id,
                )
                .group_by(
                    Organization.organization_id,
                    Organization.name,
                    Organization.code,
                    Organization.industry,
                    Organization.is_active,
                )
                .order_by(
                    Organization.name,
                )
            ).all()

        overview = []

        for row in rows:
            total = int(row.total_cases or 0)
            resolved = int(row.resolved_cases or 0)
            escalated = int(row.escalated_cases or 0)

            resolution_rate = (
                round((resolved / total) * 100, 1)
                if total
                else 0.0
            )

            overview.append(
                {
                    "organization_id": row.organization_id,
                    "name": row.name,
                    "code": row.code,
                    "industry": row.industry,
                    "is_active": row.is_active,
                    "total_cases": total,
                    "resolved_cases": resolved,
                    "escalated_cases": escalated,
                    "resolution_rate": resolution_rate,
                }
            )

        return overview

    @staticmethod
    def _date_bounds(
        start_date: date,
        end_date: date,
    ) -> tuple[datetime, datetime]:
        """Return UTC bounds for an inclusive date range."""

        start = datetime.combine(
            start_date,
            time.min,
            tzinfo=UTC,
        )

        end = datetime.combine(
            end_date + timedelta(days=1),
            time.min,
            tzinfo=UTC,
        )

        return start, end

    @staticmethod
    def _trend_period_expression(
        interval: AnalyticsInterval,
        dialect_name: str,
    ):
        """Build a trend-grouping expression for the active database."""

        timestamp = Investigation.timestamp

        if dialect_name == "sqlite":
            if interval == AnalyticsInterval.WEEK:
                return func.strftime("%Y-W%W", timestamp)

            if interval == AnalyticsInterval.MONTH:
                return func.strftime("%Y-%m", timestamp)

            return func.strftime("%Y-%m-%d", timestamp)

        if dialect_name == "postgresql":
            # PostgreSQL converts timestamptz to UTC explicitly so that
            # grouping remains consistent with the UTC date boundaries.
            timestamp_utc = func.timezone("UTC", timestamp)

            if interval == AnalyticsInterval.DAY:
                return func.to_char(timestamp_utc, "YYYY-MM-DD")

            if interval == AnalyticsInterval.MONTH:
                return func.to_char(timestamp_utc, "YYYY-MM")

            if interval == AnalyticsInterval.WEEK:
                year_start = func.make_date(
                    cast(extract("year", timestamp_utc), Integer),
                    1,
                    1,
                )

                day_of_year = extract("doy", timestamp_utc)

                january_first_weekday = extract(
                    "isodow",
                    year_start,
                )

                first_monday = (
                    1 + ((8 - january_first_weekday) % 7)
                )

                week_number = case(
                    (
                        day_of_year < first_monday,
                        0,
                    ),
                    else_=(
                        func.floor(
                            (day_of_year - first_monday) / 7
                        )
                        + 1
                    ),
                )

                return func.concat(
                    func.to_char(timestamp_utc, "YYYY"),
                    "-W",
                    func.lpad(
                        cast(
                            cast(week_number, Integer),
                            String,
                        ),
                        2,
                        "0",
                    ),
                )

        raise NotImplementedError(
            "Analytics trend grouping is not supported "
            f"for database dialect: {dialect_name}"
        )

    def get_kpis(
        self,
        start_date: date,
        end_date: date,
        *,
        organization_id: str | None = None,
    ) -> dict[str, int]:
        start, end = self._date_bounds(
            start_date,
            end_date,
        )

        conditions = [
            Investigation.timestamp >= start,
            Investigation.timestamp < end,
        ]

        if organization_id is not None:
            conditions.append(
                Investigation.organization_id
                == organization_id
            )

        with self.session_factory() as session:
            investigations = session.scalars(
                select(Investigation).where(*conditions)
            ).all()

        total = len(investigations)

        resolved = sum(
            case.status == InvestigationStatus.RESOLVED.value
            for case in investigations
        )

        waiting = sum(
            case.status == InvestigationStatus.WAITING.value
            for case in investigations
        )

        technical = sum(
            case.status
            == InvestigationStatus.TECHNICAL_INVESTIGATION.value
            for case in investigations
        )

        escalated = sum(
            case.status == InvestigationStatus.ESCALATED.value
            for case in investigations
        )

        return {
            "total_cases": total,
            "resolved_cases": resolved,
            "waiting_cases": waiting,
            "technical_investigation_cases": technical,
            "escalated_cases": escalated,
        }

    def get_status_distribution(
        self,
        start_date: date,
        end_date: date,
        *,
        organization_id: str | None = None,
    ) -> list[tuple[str, int]]:
        start, end = self._date_bounds(
            start_date,
            end_date,
        )

        conditions = [
            Investigation.timestamp >= start,
            Investigation.timestamp < end,
        ]

        if organization_id is not None:
            conditions.append(
                Investigation.organization_id
                == organization_id
            )

        with self.session_factory() as session:
            rows = session.execute(
                select(
                    Investigation.status,
                    func.count(),
                )
                .where(*conditions)
                .group_by(
                    Investigation.status,
                )
                .order_by(
                    Investigation.status,
                )
            ).all()

        return list(rows)

    def get_investigator_workload(
        self,
        start_date: date,
        end_date: date,
        *,
        organization_id: str | None = None,
    ) -> list[tuple[str, str, int]]:
        start, end = self._date_bounds(
            start_date,
            end_date,
        )

        conditions = [
            Investigation.timestamp >= start,
            Investigation.timestamp < end,
        ]

        if organization_id is not None:
            conditions.append(
                Investigation.organization_id
                == organization_id
            )

        with self.session_factory() as session:
            rows = session.execute(
                select(
                    User.full_name,
                    Investigation.created_by,
                    func.count().label("case_count"),
                )
                .join(
                    Investigation,
                    User.id == Investigation.created_by,
                )
                .where(*conditions)
                .group_by(
                    User.full_name,
                    Investigation.created_by,
                )
                .order_by(
                    func.count().desc(),
                    User.full_name.asc(),
                )
            ).all()

        return list(rows)

    def get_trend(
        self,
        start_date: date,
        end_date: date,
        interval: AnalyticsInterval,
        *,
        organization_id: str | None = None,
    ) -> list[tuple[str, int]]:
        start, end = self._date_bounds(
            start_date,
            end_date,
        )

        conditions = [
            Investigation.timestamp >= start,
            Investigation.timestamp < end,
        ]

        if organization_id is not None:
            conditions.append(
                Investigation.organization_id
                == organization_id
            )

        with self.session_factory() as session:
            period_expression = self._trend_period_expression(
                interval,
                session.get_bind().dialect.name,
            )

            rows = session.execute(
                select(
                    period_expression.label("period"),
                    func.count().label("case_count"),
                )
                .where(*conditions)
                .group_by(
                    period_expression,
                )
                .order_by(
                    period_expression,
                )
            ).all()

        return list(rows)
