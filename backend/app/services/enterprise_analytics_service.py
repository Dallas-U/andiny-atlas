from __future__ import annotations

from app.core.constants import UserRole
from app.domain import User
from app.domain.enterprise_analytics import (
    BranchAnalyticsSummary,
    DepartmentAnalyticsSummary,
    EnterpriseAnalyticsSummary,
)
from app.exceptions.exceptions import AuthorizationException
from app.repositories.enterprise_analytics_repository import (
    EnterpriseAnalyticsRepository,
)


class EnterpriseAnalyticsService:
    """
    Enterprise analytics orchestration service.

    Enforces organization scope before repository access.
    """

    def __init__(
        self,
        repository: EnterpriseAnalyticsRepository,
    ) -> None:
        self.repository = repository

    @staticmethod
    def _require_organization_access(
        current_user: User,
        organization_id: str,
    ) -> None:

        if current_user.role == UserRole.SUPER_ADMIN:
            return

        if current_user.organization_id != organization_id:
            raise AuthorizationException()

    def get_organization_summary(
        self,
        organization_id: str,
        *,
        current_user: User,
    ) -> EnterpriseAnalyticsSummary:

        self._require_organization_access(
            current_user,
            organization_id,
        )

        return self.repository.get_organization_summary(
            organization_id,
        )

    def get_branch_summaries(
        self,
        organization_id: str,
        *,
        current_user: User,
    ) -> list[BranchAnalyticsSummary]:

        self._require_organization_access(
            current_user,
            organization_id,
        )

        return self.repository.list_branch_summaries(
            organization_id,
        )

    def get_department_summaries(
        self,
        branch_id: str,
        *,
        current_user: User,
    ) -> list[DepartmentAnalyticsSummary]:

        if current_user.role == UserRole.SUPER_ADMIN:
            return self.repository.list_department_summaries(
                branch_id,
            )

        if current_user.organization_id is None:
            raise AuthorizationException()

        branch_organization_id = (
            self.repository.get_branch_organization_id(
                branch_id,
            )
        )

        if branch_organization_id != current_user.organization_id:
            raise AuthorizationException()

        return self.repository.list_department_summaries(
            branch_id,
        )