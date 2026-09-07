from __future__ import annotations

from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.models import Branch as ORMBranch
from app.database.session import SessionLocal
from app.domain.branch import Branch
from app.exceptions.exceptions import PersistenceDataException


def _to_domain(branch: ORMBranch) -> Branch:
    return Branch(
        branch_id=branch.branch_id,
        organization_id=branch.organization_id,
        name=branch.name,
        code=branch.code,
        city=branch.city,
        state=branch.state,
        is_active=branch.is_active,
        created_at=branch.created_at,
    )


class BranchRepository:
    """
    Persistence layer for organizational branches.

    Follows the Atlas repository architecture:
    - repository isolation
    - session factory injection
    - SQLAlchemy exception handling
    - ORM ↔ domain conversion
    """

    def __init__(
        self,
        session_factory: Callable[[], Session] = SessionLocal,
    ) -> None:
        self.session_factory = session_factory

    def create(
        self,
        branch: Branch,
    ) -> Branch:

        record = ORMBranch(
            branch_id=branch.branch_id,
            organization_id=branch.organization_id,
            name=branch.name,
            code=branch.code,
            city=branch.city,
            state=branch.state,
            is_active=branch.is_active,
            created_at=branch.created_at,
        )

        try:
            with self.session_factory() as session:
                with session.begin():
                    session.add(record)
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Branch could not be created."
            ) from exc

        return branch

    def list_by_organization(
        self,
        organization_id: str,
    ) -> list[Branch]:

        statement = (
            select(ORMBranch)
            .where(
                ORMBranch.organization_id == organization_id,
            )
            .order_by(ORMBranch.name.asc())
        )

        try:
            with self.session_factory() as session:
                branches = session.scalars(statement).all()
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Branches could not be loaded."
            ) from exc

        return [
            _to_domain(item)
            for item in branches
        ]

    def get_by_id(
        self,
        branch_id: str,
    ) -> Branch | None:

        try:
            with self.session_factory() as session:
                branch = session.get(
                    ORMBranch,
                    branch_id,
                )
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Branch could not be loaded."
            ) from exc

        if branch is None:
            return None

        return _to_domain(branch)

    def get_by_code(
        self,
        code: str,
    ) -> Branch | None:

        statement = select(ORMBranch).where(
            ORMBranch.code == code,
        )

        try:
            with self.session_factory() as session:
                branch = session.scalars(statement).first()
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Branch could not be loaded."
            ) from exc

        if branch is None:
            return None

        return _to_domain(branch)

    def update_status(
        self,
        branch_id: str,
        *,
        is_active: bool,
    ) -> Branch | None:
        """
        Update the active state of a branch.

        Tenant authorization is enforced by the service layer
        before this repository operation is called.
        """

        try:
            with self.session_factory() as session:
                with session.begin():
                    branch = session.get(
                        ORMBranch,
                        branch_id,
                    )

                    if branch is None:
                        return None

                    branch.is_active = is_active

                session.refresh(branch)

                return _to_domain(branch)

        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Branch status could not be updated."
            ) from exc