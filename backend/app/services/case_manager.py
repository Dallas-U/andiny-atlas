from datetime import UTC, datetime
from uuid import uuid4

from app.core.types import CaseCollection, CaseRecord
from app.exceptions.exceptions import CaseNotFoundException
from app.logging.logger import logger
from app.repositories.case_repository import CaseRepository


class CaseManager:

    def __init__(self, repository: CaseRepository):
        self.repository = repository

    def investigate_case(
        self,
        case,
        engine,
        current_user,
    ):
        """Investigate a support case and save the result."""

        logger.info(
            "Starting investigation for customer '%s'.",
            case.customer_name,
        )

        result = engine.investigate(case)

        saved_case = self.save_case(
            customer_name=case.customer_name,
            phone_number=case.phone_number,
            created_by=current_user.id,
            result=result,
        )

        logger.info(
            "Investigation completed for customer '%s'.",
            case.customer_name,
        )

        return saved_case

    def _build_case(
        self,
        customer_name,
        phone_number,
        created_by,
        result,
    ) -> CaseRecord:
        """Create a new investigation record."""

        return {
            "case_id": str(uuid4()),
            "timestamp": datetime.now(UTC).isoformat(),
            "customer_name": customer_name,
            "phone_number": phone_number,
            "created_by": created_by,
            "result": result.model_dump(),
        }

    def save_case(
        self,
        customer_name,
        phone_number,
        created_by,
        result,
    ) -> CaseRecord:
        """Build and persist an investigation case."""

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
            saved_case["case_id"],
        )

        return saved_case

    def get_all_cases(self) -> CaseCollection:
        """Return all investigation cases."""

        return self.repository.get_all_cases()

    def get_case_by_id(
        self,
        case_id: str,
    ) -> CaseRecord:
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
    ) -> CaseCollection:
        """Search investigation cases."""

        return self.repository.search_cases(
            customer_name=customer_name,
            phone_number=phone_number,
        )

    def get_statistics(self) -> dict[str, int]:
        """Return investigation statistics."""

        logger.info("Generating investigation statistics.")

        statistics = self.repository.get_statistics()

        logger.info("Statistics generated successfully.")

        return statistics
