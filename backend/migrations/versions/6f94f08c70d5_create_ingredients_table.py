"""create ingredients table

Revision ID: 6f94f08c70d5
Revises: cd747e196744
Create Date: 2025-08-12 23:39:47.483935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6f94f08c70d5'
down_revision: Union[str, Sequence[str], None] = "cd747e196744"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('ingredients',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('ingredients')
