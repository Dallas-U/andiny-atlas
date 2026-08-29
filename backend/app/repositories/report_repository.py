from datetime import UTC, date, datetime, time, timedelta

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.constants import InvestigationStatus
from app.database.mappers import investigation_to_case
from app.database.models import Investigation
from app.database.session import SessionLocal
from app.domain import Case
from app.exceptions.exceptions import PersistenceDataException
from app.logging.logger import logger


class ReportRepository:
    """Reads tenant-scoped investigation data for reporting."""

    def __init__(
        self,
        session_factory=SessionLocal,
    ):
        self.session_factory = session_factory

    @staticmethod
    def _build_date_range(
        start_date: date,
        end_date: date,
    ) -> tuple[datetime, datetime]:

        start_datetime = datetime.combine(
            start_date,
            time.min,
            tzinfo=UTC,
        )

        end_datetime = datetime.combine(
            end_date + timedelta(days=1),
            time.min,
            tzinfo=UTC,
        )

        return start_datetime, end_datetime

    def get_investigation_summary_data(
        self,
        start_date: date,
        end_date: date,
        status: InvestigationStatus | None = None,
        *,
        organization_id: str | None = None,
    ) -> tuple[list[Case], dict[str, int]]:

        start_datetime, end_datetime = self._build_date_range(
            start_date=start_date,
            end_date=end_date,
        )

        logger.info(
            "Generating investigation report data from %s to %s.",
            start_date,
            end_date,
        )

        conditions = [
            Investigation.timestamp >= start_datetime,
            Investigation.timestamp < end_datetime,
        ]

        if organization_id is not None:
            conditions.append(
                Investigation.organization_id
                == organization_id
            )

        if status is not None:
            conditions.append(
                Investigation.status == status.value,
            )

        cases_statement = (
            select(Investigation)
            .where(*conditions)
            .order_by(
                Investigation.timestamp.desc(),
                Investigation.case_id.asc(),
            )
        )

        status_statement = (
            select(
                Investigation.status,
                func.count().label("case_count"),
            )
            .where(*conditions)
            .group_by(Investigation.status)
        )

        try:
            with self.session_factory() as session:
                investigations = session.scalars(
                    cases_statement,
                ).all()

                status_rows = session.execute(
                    status_statement,
                ).all()

        except SQLAlchemyError as exc:
            logger.exception(
                "Investigation report data could not be loaded.",
            )

            raise PersistenceDataException(
                "Investigation report data could not be generated."
            ) from exc

        cases = [
            investigation_to_case(investigation)
            for investigation in investigations
        ]

        counts = {
            InvestigationStatus.RESOLVED.value: 0,
            InvestigationStatus.WAITING.value: 0,
            InvestigationStatus.TECHNICAL_INVESTIGATION.value: 0,
            InvestigationStatus.ESCALATED.value: 0,
        }

        for persisted_status, case_count in status_rows:
            if persisted_status in counts:
                counts[persisted_status] = case_count

        summary = {
            "total_cases": len(cases),
            "resolved_cases": counts[
                InvestigationStatus.RESOLVED.value
            ],
            "waiting_cases": counts[
                InvestigationStatus.WAITING.value
            ],
            "technical_investigation_cases": counts[
                InvestigationStatus.TECHNICAL_INVESTIGATION.value
            ],
            "escalated_cases": counts[
                InvestigationStatus.ESCALATED.value
            ],
        }

        return cases, summary