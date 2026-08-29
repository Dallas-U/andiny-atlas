from __future__ import annotations

from app.core.constants import UserRole
from app.domain import User
from app.exceptions.exceptions import AuthorizationException
from app.models.analytics import (
    AnalyticsInterval,
    InvestigationAnalyticsKpis,
    InvestigationTrendItem,
    InvestigatorWorkloadItem,
    StatusDistributionItem,
)
from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:
    """Business logic for tenant-scoped investigation analytics."""

    def __init__(
        self,
        repository: AnalyticsRepository,
    ) -> None:
        self.repository = repository

    @staticmethod
    def _percentage(
        count: int,
        total: int,
    ) -> float:
        """Return a percentage rounded to one decimal place."""

        if total == 0:
            return 0.0

        return round((count / total) * 100, 1)

    @staticmethod
    def _organization_scope(
        current_user: User,
        requested_organization_id: str | None = None,
    ) -> str | None:
        """
        Resolve the organization scope for an analytics request.

        Super Admin operates at platform scope and may explicitly request
        an organization.

        Customer users are always restricted to their authenticated
        organization. A client-supplied organization ID cannot override
        that scope.
        """

        if current_user.role == UserRole.SUPER_ADMIN:
            return requested_organization_id

        if current_user.organization_id is None:
            raise AuthorizationException()

        if (
            requested_organization_id is not None
            and requested_organization_id != current_user.organization_id
        ):
            raise AuthorizationException()

        return current_user.organization_id

    def get_kpis(
        self,
        start_date,
        end_date,
        *,
        current_user: User,
        organization_id: str | None = None,
    ) -> InvestigationAnalyticsKpis:
        scope = self._organization_scope(
            current_user,
            organization_id,
        )

        data = self.repository.get_kpis(
            start_date,
            end_date,
            organization_id=scope,
        )

        total = data["total_cases"]

        return InvestigationAnalyticsKpis(
            total_cases=total,
            resolved_cases=data["resolved_cases"],
            waiting_cases=data["waiting_cases"],
            technical_investigation_cases=data[
                "technical_investigation_cases"
            ],
            escalated_cases=data["escalated_cases"],
            resolution_rate=self._percentage(
                data["resolved_cases"],
                total,
            ),
            escalation_rate=self._percentage(
                data["escalated_cases"],
                total,
            ),
        )

    def get_status_distribution(
        self,
        start_date,
        end_date,
        *,
        current_user: User,
        organization_id: str | None = None,
    ) -> list[StatusDistributionItem]:

        scope = self._organization_scope(
            current_user,
            organization_id,
        )

        rows = self.repository.get_status_distribution(
            start_date,
            end_date,
            organization_id=scope,
        )

        total = sum(
            count
            for _, count in rows
        )

        return [
            StatusDistributionItem(
                status=status,
                count=count,
                percentage=self._percentage(
                    count,
                    total,
                ),
            )
            for status, count in rows
        ]

    def get_investigator_workload(
        self,
        start_date,
        end_date,
        *,
        current_user: User,
        organization_id: str | None = None,
    ) -> list[InvestigatorWorkloadItem]:

        scope = self._organization_scope(
            current_user,
            organization_id,
        )

        rows = self.repository.get_investigator_workload(
            start_date,
            end_date,
            organization_id=scope,
        )

        return [
            InvestigatorWorkloadItem(
                investigator_name=name,
                investigator_id=user_id,
                count=count,
            )
            for name, user_id, count in rows
        ]

    def get_trend(
        self,
        start_date,
        end_date,
        interval: AnalyticsInterval,
        *,
        current_user: User,
        organization_id: str | None = None,
    ) -> list[InvestigationTrendItem]:

        scope = self._organization_scope(
            current_user,
            organization_id,
        )

        rows = self.repository.get_trend(
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            organization_id=scope,
        )

        return [
            InvestigationTrendItem(
                period=str(period),
                count=count,
            )
            for period, count in rows
        ]