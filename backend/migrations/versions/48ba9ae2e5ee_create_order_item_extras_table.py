"""create order_item_extras table

Revision ID: 48ba9ae2e5ee
Revises: 4998157f1334
Create Date: 2025-08-12 23:39:47.483935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '48ba9ae2e5ee'
down_revision: Union[str, Sequence[str], None] = '4998157f1334'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('order_item_extras',
        sa.Column('order_item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('extra_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('extra_price', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(['extra_id'], ['extras.id'], ),
        sa.ForeignKeyConstraint(['order_item_id'], ['order_items.id'], ),
        sa.PrimaryKeyConstraint('order_item_id', 'extra_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('order_item_extras')
