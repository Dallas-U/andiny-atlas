"""create organizations table

Revision ID: 660a982144a1
Revises: 3be2e2af0ab7
Create Date: 2026-08-14 18:12:49.480831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '660a982144a1'
down_revision: Union[str, Sequence[str], None] = '3be2e2af0ab7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "organizations",
        sa.Column(
            "organization_id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "code",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "industry",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "contact_email",
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
        sa.PrimaryKeyConstraint("organization_id"),
    )

    op.create_index(
        op.f("ix_organizations_code"),
        "organizations",
        ["code"],
        unique=True,
    )

    op.create_index(
        op.f("ix_organizations_name"),
        "organizations",
        ["name"],
        unique=True,
    )

    # SQLite requires batch mode when adding foreign keys
    with op.batch_alter_table(
        "investigations",
        recreate="always",
    ) as batch_op:

        batch_op.add_column(
            sa.Column(
                "organization_id",
                sa.String(length=36),
                nullable=True,
            )
        )

        batch_op.create_index(
            "ix_investigations_organization_id",
            ["organization_id"],
            unique=False,
        )

        batch_op.create_foreign_key(
            "fk_investigations_organization_id_organizations",
            "organizations",
            ["organization_id"],
            ["organization_id"],
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table(
        "investigations",
        recreate="always",
    ) as batch_op:

        batch_op.drop_constraint(
            "fk_investigations_organization_id_organizations",
            type_="foreignkey",
        )

        batch_op.drop_index(
            "ix_investigations_organization_id",
        )

        batch_op.drop_column(
            "organization_id",
        )

    op.drop_index(
        op.f("ix_organizations_name"),
        table_name="organizations",
    )

    op.drop_index(
        op.f("ix_organizations_code"),
        table_name="organizations",
    )

    op.drop_table("organizations")