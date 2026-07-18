from dataclasses import dataclass
from datetime import UTC, datetime
from math import ceil
from uuid import uuid4

from app.core.constants import InvestigationStatus
from app.domain import (
    Case,
    Customer,
    InvestigationResult,
)
from app.exceptions.exceptions import CaseNotFoundException
from app.logging.logger import logger
from app.models.query import CaseQuery
from app.repositories.case_repository import CaseRepository


@dataclass(frozen=True, slots=True)
class CasePage:
    """Application-layer result for a paginated case query."""

    page: int
    page_size: int
    total_records: int
    total_pages: int
    cases: tuple[Case, ...]

    @property
    def returned_records(self) -> int:
        """Return the number of cases included in this page."""

        return len(self.cases)


class CaseManager:
    """Business logic for investigation cases."""

    def __init__(
        self,
        repository: CaseRepository,
    ):
        self.repository = repository

    def investigate_case(
        self,
        support_case,
        engine,
        created_by: str,
    ) -> Case:
        """Investigate and persist a support case."""

        logger.info(
            "Starting investigation for customer '%s'.",
            support_case.customer_name,
        )

        result = engine.investigate(support_case)

        saved_case = self.save_case(
            customer_name=support_case.customer_name,
            phone_number=support_case.phone_number,
            created_by=created_by,
            result=result,
        )

        logger.info(
            "Investigation completed for customer '%s'.",
            support_case.customer_name,
        )

        return saved_case

    @staticmethod
    def _to_domain_status(
        status: InvestigationStatus | str,
    ) -> InvestigationStatus:
        """Convert an investigation status into its domain enum."""

        if isinstance(status, InvestigationStatus):
            return status

        return InvestigationStatus(status)

    def _build_case(
        self,
        customer_name: str,
        phone_number: str,
        created_by: str,
        result,
    ) -> Case:
        """Create a new domain investigation case."""

        return Case(
            case_id=str(uuid4()),
            timestamp=datetime.now(UTC),
            customer=Customer(
                name=customer_name,
                phone_number=phone_number,
            ),
            created_by=created_by,
            result=InvestigationResult(
                status=self._to_domain_status(result.status),
                reason=result.reason,
                next_action=result.next_action,
            ),
        )

    def save_case(
        self,
        customer_name: str,
        phone_number: str,
        created_by: str,
        result,
    ) -> Case:
        """Build and persist a domain investigation case."""

        logger.info("Creating a new investigation record.")

        case = self._build_case(
            customer_name=customer_name,
            phone_number=phone_number,
            created_by=created_by,
            result=result,
        )

        saved_case = self.repository.create_case(case)

        logger.info(
            "Investigation '%s' saved successfully.",
            saved_case.case_id,
        )

        return saved_case

    def get_all_cases(self) -> list[Case]:
        """Return all investigation cases."""

        return self.repository.get_all_cases()

    def get_case_by_id(
        self,
        case_id: str,
    ) -> Case:
        """Return one investigation case by ID."""

        logger.info(
            "Searching for case '%s'.",
            case_id,
        )

        case = self.repository.get_case_by_id(case_id)

        if case is None:
            raise CaseNotFoundException(case_id)

        logger.info(
            "Case '%s' found.",
            case_id,
        )

        return case

    def search_cases(
        self,
        customer_name: str | None = None,
        phone_number: str | None = None,
    ) -> list[Case]:
        """Search investigation cases using legacy filters."""

        return self.repository.search_cases(
            customer_name=customer_name,
            phone_number=phone_number,
        )

    def query_cases(
        self,
        query: CaseQuery,
    ) -> CasePage:
        """Return filtered, sorted, and paginated domain cases."""

        cases, total_records = self.repository.query_cases(
            query,
        )

        total_pages = ceil(total_records / query.page_size) if total_records > 0 else 0

        page = CasePage(
            page=query.page,
            page_size=query.page_size,
            total_records=total_records,
            total_pages=total_pages,
            cases=tuple(cases),
        )

        logger.info(
            "Generated page %d of investigation query results.",
            query.page,
        )

        return page

    def update_case(
        self,
        case_id: str,
        status: InvestigationStatus | str,
        reason: str,
        next_action: str,
        current_user_id: str,
    ) -> Case:
        """Update an investigation owned by the authenticated user."""

        logger.info(
            "Preparing to update investigation '%s'.",
            case_id,
        )

        existing_case = self.repository.get_case_by_id(
            case_id,
        )

        if existing_case is None:
            raise CaseNotFoundException(case_id)

        if existing_case.created_by != current_user_id:
            logger.warning(
                "User '%s' attempted to update investigation '%s' "
                "owned by another user.",
                current_user_id,
                case_id,
            )

            # Do not reveal another user's investigation through
            # the update endpoint.
            raise CaseNotFoundException(case_id)

        domain_status = self._to_domain_status(status)

        updated_case = self.repository.update_case(
            case_id=case_id,
            status=domain_status.value,
            reason=reason.strip(),
            next_action=next_action.strip(),
        )

        if updated_case is None:
            raise CaseNotFoundException(case_id)

        logger.info(
            "Investigation '%s' updated successfully by user '%s'.",
            case_id,
            current_user_id,
        )

        return updated_case

    def get_statistics(self) -> dict[str, int]:
        """Return investigation statistics."""

        logger.info("Generating investigation statistics.")

        statistics = self.repository.get_statistics()

        logger.info("Statistics generated successfully.")

        return statistics
