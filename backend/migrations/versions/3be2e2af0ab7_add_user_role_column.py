"""add user role column

Revision ID: 3be2e2af0ab7
Revises: 9ecc0c4c40be
Create Date: 2026-07-20

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic.
revision: str = "3be2e2af0ab7"
down_revision: str | Sequence[str] | None = "9ecc0c4c40be"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add the hierarchical RBAC role column to application users."""

    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=20),
            server_default="AGENT",
            nullable=False,
        ),
    )

    op.create_index(
        op.f("ix_users_role"),
        "users",
        ["role"],
        unique=False,
    )


def downgrade() -> None:
    """Remove the hierarchical RBAC role column from application users."""

    op.drop_index(
        op.f("ix_users_role"),
        table_name="users",
    )

    op.drop_column(
        "users",
        "role",
    )
