from __future__ import annotations

from collections.abc import Callable

from sqlalchemy import case, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.models import (
    Branch,
    Department,
    Investigation,
)
from app.database.session import SessionLocal
from app.domain.enterprise_analytics import (
    BranchAnalyticsSummary,
    DepartmentAnalyticsSummary,
    EnterpriseAnalyticsSummary,
)
from app.exceptions.exceptions import PersistenceDataException


class EnterpriseAnalyticsRepository:
    """
    Enterprise analytics aggregation repository.

    Responsible for organization, branch, and department
    level operational metrics.
    """

    def __init__(
        self,
        session_factory: Callable[[], Session] = SessionLocal,
    ) -> None:
        self.session_factory = session_factory

    def get_branch_organization_id(
        self,
        branch_id: str,
    ) -> str | None:

        try:
            with self.session_factory() as session:
                return session.scalar(
                    select(
                        Branch.organization_id,
                    ).where(
                        Branch.branch_id == branch_id,
                    )
                )
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Branch ownership could not be loaded."
            ) from exc

    def get_organization_summary(
        self,
        organization_id: str,
    ) -> EnterpriseAnalyticsSummary:

        try:
            with self.session_factory() as session:

                total = session.scalar(
                    select(func.count())
                    .select_from(Investigation)
                    .where(
                        Investigation.organization_id
                        == organization_id,
                    )
                ) or 0

                resolved = session.scalar(
                    select(func.count())
                    .select_from(Investigation)
                    .where(
                        Investigation.organization_id
                        == organization_id,
                        Investigation.status == "Resolved",
                    )
                ) or 0

                waiting = session.scalar(
                    select(func.count())
                    .select_from(Investigation)
                    .where(
                        Investigation.organization_id
                        == organization_id,
                        Investigation.status == "Waiting",
                    )
                ) or 0

                technical = session.scalar(
                    select(func.count())
                    .select_from(Investigation)
                    .where(
                        Investigation.organization_id
                        == organization_id,
                        Investigation.status
                        == "Technical Investigation",
                    )
                ) or 0

                escalated = session.scalar(
                    select(func.count())
                    .select_from(Investigation)
                    .where(
                        Investigation.organization_id
                        == organization_id,
                        Investigation.status == "Escalated",
                    )
                ) or 0

        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Organization analytics could not be loaded."
            ) from exc

        resolution_rate = (
            (resolved / total) * 100
            if total
            else 0.0
        )

        escalation_rate = (
            (escalated / total) * 100
            if total
            else 0.0
        )

        return EnterpriseAnalyticsSummary(
            total_cases=total,
            resolved_cases=resolved,
            waiting_cases=waiting,
            technical_investigation_cases=technical,
            escalated_cases=escalated,
            resolution_rate=round(
                resolution_rate,
                1,
            ),
            escalation_rate=round(
                escalation_rate,
                1,
            ),
        )

    def list_branch_summaries(
        self,
        organization_id: str,
    ) -> list[BranchAnalyticsSummary]:

        statement = (
            select(
                Branch.branch_id,
                Branch.name,
                func.count(
                    Investigation.case_id
                ).label("total_cases"),
                func.sum(
                    case(
                        (
                            Investigation.status == "Resolved",
                            1,
                        ),
                        else_=0,
                    )
                ).label("resolved_cases"),
                func.sum(
                    case(
                        (
                            Investigation.status == "Escalated",
                            1,
                        ),
                        else_=0,
                    )
                ).label("escalated_cases"),
            )
            .outerjoin(
                Investigation,
                Investigation.branch_id
                == Branch.branch_id,
            )
            .where(
                Branch.organization_id == organization_id,
            )
            .group_by(
                Branch.branch_id,
                Branch.name,
            )
            .order_by(
                Branch.name.asc(),
            )
        )

        try:
            with self.session_factory() as session:
                rows = session.execute(statement).all()
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Branch analytics could not be loaded."
            ) from exc

        summaries = []

        for (
            branch_id,
            branch_name,
            total,
            resolved,
            escalated,
        ) in rows:

            total = int(total or 0)
            resolved = int(resolved or 0)
            escalated = int(escalated or 0)

            escalation_rate = (
                (escalated / total) * 100
                if total
                else 0.0
            )

            summaries.append(
                BranchAnalyticsSummary(
                    branch_id=branch_id,
                    branch_name=branch_name,
                    total_cases=total,
                    resolved_cases=resolved,
                    escalation_rate=round(
                        escalation_rate,
                        1,
                    ),
                )
            )

        return summaries

    def list_department_summaries(
        self,
        branch_id: str,
    ) -> list[DepartmentAnalyticsSummary]:

        statement = (
            select(
                Department.department_id,
                Department.name,
                func.count(
                    Investigation.case_id
                ).label("total_cases"),
                func.sum(
                    case(
                        (
                            Investigation.status == "Resolved",
                            1,
                        ),
                        else_=0,
                    )
                ).label("resolved_cases"),
                func.sum(
                    case(
                        (
                            Investigation.status == "Escalated",
                            1,
                        ),
                        else_=0,
                    )
                ).label("escalated_cases"),
            )
            .outerjoin(
                Investigation,
                Investigation.department_id
                == Department.department_id,
            )
            .where(
                Department.branch_id == branch_id,
            )
            .group_by(
                Department.department_id,
                Department.name,
            )
            .order_by(
                Department.name.asc(),
            )
        )

        try:
            with self.session_factory() as session:
                rows = session.execute(statement).all()
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Department analytics could not be loaded."
            ) from exc

        summaries = []

        for (
            department_id,
            department_name,
            total,
            resolved,
            escalated,
        ) in rows:

            total = int(total or 0)
            resolved = int(resolved or 0)
            escalated = int(escalated or 0)

            escalation_rate = (
                (escalated / total) * 100
                if total
                else 0.0
            )

            summaries.append(
                DepartmentAnalyticsSummary(
                    department_id=department_id,
                    department_name=department_name,
                    total_cases=total,
                    resolved_cases=resolved,
                    escalation_rate=round(
                        escalation_rate,
                        1,
                    ),
                )
            )

        return summaries