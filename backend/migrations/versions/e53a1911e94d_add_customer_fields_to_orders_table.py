"""add customer fields to orders table

Revision ID: e53a1911e94d
Revises: 48ba9ae2e5ee
Create Date: 2025-08-13 04:16:16.387434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e53a1911e94d'
down_revision: Union[str, Sequence[str], None] = '48ba9ae2e5ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('orders', sa.Column('customer_name', sa.String(), nullable=False, server_default=''))
    op.add_column('orders', sa.Column('customer_address', sa.String(), nullable=False, server_default=''))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('orders', 'customer_address')
    op.drop_column('orders', 'customer_name')
