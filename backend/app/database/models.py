from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import UserRole
from app.database.database import Base


class Investigation(Base):
    """Database representation of a support investigation."""

    __tablename__ = "investigations"

    case_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    customer_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    phone_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    created_by: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True,
    )

    organization_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("organizations.organization_id"),
        nullable=True,
        index=True,
    )

    branch_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey(
            "branches.branch_id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    department_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey(
            "departments.department_id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )    
    
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    reason: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    next_action: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )


class CaseHistory(Base):
    """Append-only audit history for investigation changes."""

    __tablename__ = "investigation_history"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    case_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "investigations.case_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    reason: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    next_action: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    changed_by: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True,
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )


class User(Base):
    """Database representation of an application user."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default=UserRole.AGENT.value,
        server_default=UserRole.AGENT.value,
        nullable=False,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

class Organization(Base):
    """
    Database representation of an organization tenant.
    """

    __tablename__ = "organizations"

    organization_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    industry: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    contact_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )


class Branch(Base):
    """
    Database representation of an organizational branch.
    """

    __tablename__ = "branches"

    branch_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    organization_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "organizations.organization_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )


class Department(Base):
    """
    Database representation of a department within a branch.
    """

    __tablename__ = "departments"

    department_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    organization_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "organizations.organization_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "branches.branch_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )   