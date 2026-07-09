from app.core.constants import (
    STATUS_RESOLVED,
    STATUS_WAITING,
    STATUS_TECHNICAL_INVESTIGATION,
    STATUS_ESCALATED,
)
from datetime import UTC, datetime
from uuid import uuid4

from app.core.types import CaseCollection, CaseRecord
from app.exceptions.exceptions import CaseNotFoundException
from app.logging.logger import logger
from app.repositories.case_repository import CaseRepository


class CaseManager:

    def __init__(self, repository: CaseRepository):
        self.repository = repository

    def investigate_case(self, case, engine):
        """Investigate a support case and save the result."""

        logger.info(
            "Starting investigation for customer '%s'.",
            case.customer_name,
        )

        result = engine.investigate(case)

        saved_case = self.save_case(
            customer_name=case.customer_name,
            phone_number=case.phone_number,
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
        result,
    ) -> CaseRecord:
        """Create a new investigation record."""

        return {
            "case_id": str(uuid4()),
            "timestamp": datetime.now(UTC).isoformat(),
            "customer_name": customer_name,
            "phone_number": phone_number,
            "result": result.model_dump(),
        }

    def save_case(
        self,
        customer_name,
        phone_number,
        result,
    ):

        investigations = self.repository.load_cases()

        logger.info("Creating a new investigation record.")

        case = self._build_case(
            customer_name=customer_name,
            phone_number=phone_number,
            result=result,
        )

        investigations.append(case)

        self.repository.save_cases(investigations)

        logger.info(
            "Investigation '%s' saved successfully.",
            case["case_id"],
        )

        return case

    def get_all_cases(self) -> CaseCollection:

        return self.repository.load_cases()

    def get_case_by_id(
        self,
        case_id,
    ):

        logger.info(
            "Searching for case '%s'.",
            case_id,
        )

        investigations = self.get_all_cases()

        for case in investigations:

            if case["case_id"] == case_id:

                logger.info(
                    "Case '%s' found.",
                    case_id,
                )

                return case

        raise CaseNotFoundException(case_id)

    def search_cases(
        self,
        customer_name=None,
        phone_number=None,
    ) -> CaseCollection:

        investigations = self.get_all_cases()

        results = investigations

        if customer_name:

            results = [
                case
                for case in results
                if case["customer_name"].lower() == customer_name.lower()
            ]

        if phone_number:

            results = [case for case in results if case["phone_number"] == phone_number]

        return results

    def get_statistics(self):

        logger.info("Generating investigation statistics.")

        cases = self.get_all_cases()

        total = len(cases)

        resolved = 0
        pending = 0
        escalated = 0

        for case in cases:

            status = case["result"]["status"]

            if status == STATUS_RESOLVED:
                resolved += 1

            elif status in (
                STATUS_WAITING,
                STATUS_TECHNICAL_INVESTIGATION,
            ):
                pending += 1

            elif status == STATUS_ESCALATED:
                escalated += 1

        logger.info("Statistics generated successfully.")

        return {
            "total_cases": total,
            "resolved_cases": resolved,
            "pending_cases": pending,
            "escalated_cases": escalated,
        }
