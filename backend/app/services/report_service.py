from __future__ import annotations

from datetime import date

from app.core.constants import InvestigationStatus, UserRole
from app.domain import Case, User
from app.exceptions.exceptions import AuthorizationException
from app.logging.logger import logger
from app.repositories.report_repository import ReportRepository


class ReportService:
    """Business logic for tenant-scoped investigation reports."""

    def __init__(
        self,
        repository: ReportRepository,
    ):
        self.repository = repository

    @staticmethod
    def _organization_scope(
        current_user: User,
        requested_organization_id: str | None = None,
    ) -> str | None:

        if current_user.role == UserRole.SUPER_ADMIN:
            return requested_organization_id

        if current_user.organization_id is None:
            raise AuthorizationException()

        if (
            requested_organization_id is not None
            and requested_organization_id
            != current_user.organization_id
        ):
            raise AuthorizationException()

        return current_user.organization_id

    def get_investigation_summary(
        self,
        start_date: date,
        end_date: date,
        status: InvestigationStatus | None = None,
        *,
        current_user: User,
        organization_id: str | None = None,
    ) -> tuple[list[Case], dict[str, int]]:

        scope = self._organization_scope(
            current_user,
            organization_id,
        )

        logger.info(
            "Preparing tenant-scoped investigation report "
            "from %s to %s.",
            start_date,
            end_date,
        )

        cases, summary = (
            self.repository.get_investigation_summary_data(
                start_date=start_date,
                end_date=end_date,
                status=status,
                organization_id=scope,
            )
        )

        logger.info(
            "Investigation summary report prepared successfully.",
        )

        return cases, summary