"""Create initial users and investigations schema."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "3765eb6de05d"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the initial application tables."""

    op.create_table(
        "investigations",
        sa.Column(
            "case_id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "customer_name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "phone_number",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "reason",
            sa.String(length=500),
            nullable=False,
        ),
        sa.Column(
            "next_action",
            sa.String(length=500),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("case_id"),
    )

    op.create_index(
        "ix_investigations_customer_name",
        "investigations",
        ["customer_name"],
        unique=False,
    )

    op.create_index(
        "ix_investigations_phone_number",
        "investigations",
        ["phone_number"],
        unique=False,
    )

    op.create_index(
        "ix_investigations_status",
        "investigations",
        ["status"],
        unique=False,
    )

    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "full_name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "hashed_password",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True,
    )


def downgrade() -> None:
    """Remove the initial application tables."""

    op.drop_index(
        "ix_users_email",
        table_name="users",
    )
    op.drop_table("users")

    op.drop_index(
        "ix_investigations_status",
        table_name="investigations",
    )
    op.drop_index(
        "ix_investigations_phone_number",
        table_name="investigations",
    )
    op.drop_index(
        "ix_investigations_customer_name",
        table_name="investigations",
    )
    op.drop_table("investigations")
