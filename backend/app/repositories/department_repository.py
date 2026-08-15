from __future__ import annotations

from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.models import Department as ORMDepartment
from app.database.session import SessionLocal
from app.domain.department import Department
from app.exceptions.exceptions import PersistenceDataException


def _to_domain(
    department: ORMDepartment,
) -> Department:
    return Department(
        department_id=department.department_id,
        organization_id=department.organization_id,
        branch_id=department.branch_id,
        name=department.name,
        code=department.code,
        is_active=department.is_active,
        created_at=department.created_at,
    )


class DepartmentRepository:
    """
    Persistence layer for organizational departments.

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
        department: Department,
    ) -> Department:

        record = ORMDepartment(
            department_id=department.department_id,
            organization_id=department.organization_id,
            branch_id=department.branch_id,
            name=department.name,
            code=department.code,
            is_active=department.is_active,
            created_at=department.created_at,
        )

        try:
            with self.session_factory() as session:
                with session.begin():
                    session.add(record)
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Department could not be created."
            ) from exc

        return department

    def list_by_branch(
        self,
        branch_id: str,
    ) -> list[Department]:

        statement = (
            select(ORMDepartment)
            .where(
                ORMDepartment.branch_id == branch_id,
            )
            .order_by(ORMDepartment.name.asc())
        )

        try:
            with self.session_factory() as session:
                departments = session.scalars(statement).all()
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Departments could not be loaded."
            ) from exc

        return [_to_domain(item) for item in departments]

    def get_by_id(
        self,
        department_id: str,
    ) -> Department | None:

        try:
            with self.session_factory() as session:
                department = session.get(
                    ORMDepartment,
                    department_id,
                )
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Department could not be loaded."
            ) from exc

        if department is None:
            return None

        return _to_domain(department)

    def get_by_code(
        self,
        code: str,
    ) -> Department | None:

        statement = select(ORMDepartment).where(
            ORMDepartment.code == code,
        )

        try:
            with self.session_factory() as session:
                department = session.scalars(statement).first()
        except SQLAlchemyError as exc:
            raise PersistenceDataException(
                "Department could not be loaded."
            ) from exc

        if department is None:
            return None

        return _to_domain(department)