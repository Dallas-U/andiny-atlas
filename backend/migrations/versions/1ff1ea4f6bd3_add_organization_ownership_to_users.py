"""add organization ownership to users

Revision ID: 1ff1ea4f6bd3
Revises: 03af6fc47af5
Create Date: 2026-08-29
"""

from alembic import op
import sqlalchemy as sa


revision = "1ff1ea4f6bd3"
down_revision = "03af6fc47af5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    indexes = {
        index["name"]
        for index in inspector.get_indexes("users")
    }

    foreign_keys = inspector.get_foreign_keys("users")

    existing_fk_names = {
        fk.get("name")
        for fk in foreign_keys
    }

    # SQLite requires batch mode for adding foreign keys.
    with op.batch_alter_table(
        "users",
        recreate="always",
    ) as batch_op:

        if "organization_id" not in columns:
            batch_op.add_column(
                sa.Column(
                    "organization_id",
                    sa.String(length=36),
                    nullable=True,
                ),
            )

        if "ix_users_organization_id" not in indexes:
            batch_op.create_index(
                "ix_users_organization_id",
                ["organization_id"],
                unique=False,
            )

        if (
            "fk_users_organization_id_organizations"
            not in existing_fk_names
        ):
            batch_op.create_foreign_key(
                "fk_users_organization_id_organizations",
                "organizations",
                ["organization_id"],
                ["organization_id"],
                ondelete="SET NULL",
            )


def downgrade() -> None:
    with op.batch_alter_table(
        "users",
        recreate="always",
    ) as batch_op:

        batch_op.drop_constraint(
            "fk_users_organization_id_organizations",
            type_="foreignkey",
        )

        batch_op.drop_index(
            "ix_users_organization_id",
        )

        batch_op.drop_column(
            "organization_id",
        )