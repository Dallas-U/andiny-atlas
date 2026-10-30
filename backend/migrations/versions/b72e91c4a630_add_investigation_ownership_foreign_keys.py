"""Add missing investigation branch and department foreign keys.

Revision ID: b72e91c4a630
Revises: 1ff1ea4f6bd3

Adds the foreign-key constraints required by the current SQLAlchemy models.
Existing columns and indexes are preserved.
"""

from typing import Sequence, Union

from alembic import op


revision: str = "b72e91c4a630"
down_revision: Union[str, Sequence[str], None] = "1ff1ea4f6bd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_investigations_branch_id_branches",
        "investigations",
        "branches",
        ["branch_id"],
        ["branch_id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_investigations_department_id_departments",
        "investigations",
        "departments",
        ["department_id"],
        ["department_id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_investigations_department_id_departments",
        "investigations",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_investigations_branch_id_branches",
        "investigations",
        type_="foreignkey",
    )
