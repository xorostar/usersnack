"""create extras table

Revision ID: dfd022b4ddee
Revises: 7d4d7483230e
Create Date: 2025-08-12 23:39:47.483935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dfd022b4ddee'
down_revision: Union[str, Sequence[str], None] = '7d4d7483230e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('extras',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('extras')
