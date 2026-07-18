from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.constants import InvestigationStatus
from app.database.mappers import (
    case_to_investigation,
    investigation_to_case,
)
from app.database.models import Investigation
from app.database.session import SessionLocal
from app.domain import Case
from app.exceptions.exceptions import PersistenceDataException
from app.logging.logger import logger
from app.models.query import (
    CaseQuery,
    CaseSortField,
    SortOrder,
)


class CaseRepository:
    """Handles persistence of investigation cases using SQLAlchemy."""

    def __init__(
        self,
        session_factory: Callable[[], Session] = SessionLocal,
    ):
        self.session_factory = session_factory

    def create_case(
        self,
        case: Case,
    ) -> Case:
        """Persist a single domain investigation case."""

        logger.info(
            "Saving investigation '%s' to SQLite.",
            case.case_id,
        )

        investigation = case_to_investigation(case)

        try:
            with self.session_factory() as session:
                with session.begin():
                    session.add(investigation)

        except SQLAlchemyError as exc:
            logger.exception(
                "Investigation '%s' could not be saved to SQLite.",
                case.case_id,
            )

            raise PersistenceDataException(
                "Persisted investigation data could not be saved."
            ) from exc

        logger.info(
            "Investigation '%s' saved successfully to SQLite.",
            case.case_id,
        )

        return case

    def get_all_cases(self) -> list[Case]:
        """Return all persisted investigation cases."""

        logger.info("Loading investigation cases from SQLite.")

        statement = select(Investigation).order_by(
            Investigation.timestamp,
            Investigation.case_id,
        )

        try:
            with self.session_factory() as session:
                investigations = session.scalars(statement).all()

        except SQLAlchemyError as exc:
            logger.exception("Investigation data could not be loaded from SQLite.")

            raise PersistenceDataException(
                "Persisted investigation data is invalid and could not be read."
            ) from exc

        cases = [
            investigation_to_case(investigation) for investigation in investigations
        ]

        logger.info(
            "Loaded %d investigation case(s) from SQLite.",
            len(cases),
        )

        return cases

    def get_case_by_id(
        self,
        case_id: str,
    ) -> Case | None:
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

        return investigation_to_case(investigation)

    def search_cases(
        self,
        customer_name: str | None = None,
        phone_number: str | None = None,
    ) -> list[Case]:
        """Search persisted investigations using optional filters."""

        logger.info("Searching investigation cases in SQLite.")

        statement = select(Investigation)

        if customer_name:
            statement = statement.where(
                func.lower(Investigation.customer_name) == customer_name.strip().lower()
            )

        if phone_number:
            statement = statement.where(
                Investigation.phone_number == phone_number.strip()
            )

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
            investigation_to_case(investigation) for investigation in investigations
        ]

    def query_cases(
        self,
        query: CaseQuery,
    ) -> tuple[list[Case], int]:
        """Filter, sort, and paginate persisted investigation cases."""

        logger.info(
            "Querying investigation cases: page=%d, page_size=%d.",
            query.page,
            query.page_size,
        )

        conditions = []

        if query.customer_name:
            conditions.append(
                func.lower(Investigation.customer_name)
                == query.customer_name.strip().lower()
            )

        if query.phone_number:
            conditions.append(Investigation.phone_number == query.phone_number.strip())

        if query.created_by:
            conditions.append(Investigation.created_by == query.created_by)

        if query.status:
            conditions.append(Investigation.status == query.status.value)

        sort_columns = {
            CaseSortField.TIMESTAMP: Investigation.timestamp,
            CaseSortField.CUSTOMER_NAME: Investigation.customer_name,
            CaseSortField.PHONE_NUMBER: Investigation.phone_number,
            CaseSortField.STATUS: Investigation.status,
            CaseSortField.CREATED_BY: Investigation.created_by,
        }

        sort_column = sort_columns[query.sort_by]

        if query.sort_order is SortOrder.ASC:
            order_expression = sort_column.asc()
        else:
            order_expression = sort_column.desc()

        offset = (query.page - 1) * query.page_size

        data_statement = (
            select(Investigation)
            .where(*conditions)
            .order_by(
                order_expression,
                Investigation.case_id.asc(),
            )
            .offset(offset)
            .limit(query.page_size)
        )

        count_statement = (
            select(func.count()).select_from(Investigation).where(*conditions)
        )

        try:
            with self.session_factory() as session:
                total_records = session.scalar(count_statement) or 0
                investigations = session.scalars(data_statement).all()

        except SQLAlchemyError as exc:
            logger.exception("Investigation cases could not be queried in SQLite.")

            raise PersistenceDataException(
                "Persisted investigation data is invalid and could not be read."
            ) from exc

        cases = [
            investigation_to_case(investigation) for investigation in investigations
        ]

        logger.info(
            "Returned %d of %d matching investigation case(s).",
            len(cases),
            total_records,
        )

        return cases, total_records

    def update_case(
        self,
        case_id: str,
        status: str,
        reason: str,
        next_action: str,
    ) -> Case | None:
        """Update the editable fields of an investigation case."""

        logger.info(
            "Updating investigation '%s' in SQLite.",
            case_id,
        )

        try:
            with self.session_factory() as session:
                with session.begin():
                    investigation = session.get(
                        Investigation,
                        case_id,
                    )

                    if investigation is None:
                        logger.info(
                            "Investigation '%s' was not found for update.",
                            case_id,
                        )

                        return None

                    investigation.status = status
                    investigation.reason = reason
                    investigation.next_action = next_action

                updated_case = investigation_to_case(investigation)

        except SQLAlchemyError as exc:
            logger.exception(
                "Investigation '%s' could not be updated in SQLite.",
                case_id,
            )

            raise PersistenceDataException(
                "Persisted investigation data could not be updated."
            ) from exc

        logger.info(
            "Investigation '%s' updated successfully in SQLite.",
            case_id,
        )

        return updated_case

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
