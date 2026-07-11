from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.constants import InvestigationStatus
from app.core.types import CaseCollection, CaseRecord
from app.database.mappers import (
    investigation_to_record,
    record_to_investigation,
)
from app.database.models import Investigation
from app.database.session import SessionLocal
from app.exceptions.exceptions import PersistenceDataException
from app.logging.logger import logger


class CaseRepository:
    """Handles persistence of investigation cases using SQLAlchemy."""

    def __init__(
        self,
        session_factory: Callable[[], Session] = SessionLocal,
    ):
        self.session_factory = session_factory

    def create_case(
        self,
        case: CaseRecord,
    ) -> CaseRecord:
        """Persist a single investigation case."""

        logger.info(
            "Saving investigation '%s' to SQLite.",
            case["case_id"],
        )

        investigation = record_to_investigation(case)

        try:
            with self.session_factory() as session:
                with session.begin():
                    session.add(investigation)

        except SQLAlchemyError as exc:
            logger.exception(
                "Investigation '%s' could not be saved to SQLite.",
                case["case_id"],
            )

            raise PersistenceDataException(
                "Persisted investigation data could not be saved."
            ) from exc

        logger.info(
            "Investigation '%s' saved successfully to SQLite.",
            case["case_id"],
        )

        return case

    def get_all_cases(self) -> CaseCollection:
        """Return all persisted investigation cases."""

        logger.info("Loading investigation cases from SQLite.")

        try:
            with self.session_factory() as session:
                statement = select(Investigation).order_by(
                    Investigation.timestamp,
                    Investigation.case_id,
                )

                investigations = session.scalars(statement).all()

        except SQLAlchemyError as exc:
            logger.exception("Investigation data could not be loaded from SQLite.")

            raise PersistenceDataException(
                "Persisted investigation data is invalid and could not be read."
            ) from exc

        cases = [
            investigation_to_record(investigation) for investigation in investigations
        ]

        logger.info(
            "Loaded %d investigation case(s) from SQLite.",
            len(cases),
        )

        return cases

    def get_case_by_id(
        self,
        case_id: str,
    ) -> CaseRecord | None:
        """Return an investigation case by its ID."""

        logger.info(
            "Loading investigation '%s' from SQLite.",
            case_id,
        )

        try:
            with self.session_factory() as session:
                investigation = session.get(
                    Investigation,
                    case_id,
                )

        except SQLAlchemyError as exc:
            logger.exception(
                "Investigation '%s' could not be loaded from SQLite.",
                case_id,
            )

            raise PersistenceDataException(
                "Persisted investigation data is invalid and could not be read."
            ) from exc

        if investigation is None:
            return None

        return investigation_to_record(investigation)

    def search_cases(
        self,
        customer_name: str | None = None,
        phone_number: str | None = None,
    ) -> CaseCollection:
        """Search persisted investigations using optional filters."""

        logger.info("Searching investigation cases in SQLite.")

        statement = select(Investigation)

        if customer_name:
            statement = statement.where(
                func.lower(Investigation.customer_name) == customer_name.lower()
            )

        if phone_number:
            statement = statement.where(Investigation.phone_number == phone_number)

        statement = statement.order_by(
            Investigation.timestamp,
            Investigation.case_id,
        )

        try:
            with self.session_factory() as session:
                investigations = session.scalars(statement).all()

        except SQLAlchemyError as exc:
            logger.exception("Investigation cases could not be searched in SQLite.")

            raise PersistenceDataException(
                "Persisted investigation data is invalid and could not be read."
            ) from exc

        return [
            investigation_to_record(investigation) for investigation in investigations
        ]

    def get_statistics(self) -> dict[str, int]:
        """Calculate investigation statistics using SQL queries."""

        logger.info("Calculating investigation statistics from SQLite.")

        try:
            with self.session_factory() as session:
                total = (
                    session.scalar(select(func.count()).select_from(Investigation)) or 0
                )

                resolved = (
                    session.scalar(
                        select(func.count())
                        .select_from(Investigation)
                        .where(
                            Investigation.status == InvestigationStatus.RESOLVED.value
                        )
                    )
                    or 0
                )

                pending = (
                    session.scalar(
                        select(func.count())
                        .select_from(Investigation)
                        .where(
                            Investigation.status.in_(
                                (
                                    InvestigationStatus.WAITING.value,
                                    InvestigationStatus.TECHNICAL_INVESTIGATION.value,
                                )
                            )
                        )
                    )
                    or 0
                )

                escalated = (
                    session.scalar(
                        select(func.count())
                        .select_from(Investigation)
                        .where(
                            Investigation.status == InvestigationStatus.ESCALATED.value
                        )
                    )
                    or 0
                )

        except SQLAlchemyError as exc:
            logger.exception("Investigation statistics could not be calculated.")

            raise PersistenceDataException(
                "Persisted investigation data is invalid and could not be read."
            ) from exc

        return {
            "total_cases": total,
            "resolved_cases": resolved,
            "pending_cases": pending,
            "escalated_cases": escalated,
        }
