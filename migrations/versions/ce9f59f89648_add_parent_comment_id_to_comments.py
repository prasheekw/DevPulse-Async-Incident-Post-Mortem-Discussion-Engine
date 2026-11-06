"""add parent_comment_id to comments

Revision ID: ce9f59f89648
Revises: 
Create Date: 2026-10-30 14:58:20.547921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce9f59f89648'
down_revision = "b71c9a2d4e60"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "comments",
        sa.Column("parent_comment_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_comments_parent_comment_id_comments",
        "comments",
        "comments",
        ["parent_comment_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_comments_parent_comment_id_comments",
        "comments",
        type_="foreignkey"
    )

    op.drop_column("comments", "parent_comment_id")
