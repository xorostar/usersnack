"""create orders table

Revision ID: 7d4d7483230e
Revises: 93c8dc4648de
Create Date: 2025-08-12 23:39:47.483935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7d4d7483230e'
down_revision: Union[str, Sequence[str], None] = '93c8dc4648de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE orderstatus AS ENUM ('CREATED', 'CONFIRMED', 'CANCELLED')")
    
    op.execute("CREATE TYPE currency AS ENUM ('EUR', 'USD')")
    
    op.create_table('orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', postgresql.ENUM('CREATED', 'CONFIRMED', 'CANCELLED', name='orderstatus', create_type=False), nullable=False),
        sa.Column('total_amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('currency', postgresql.ENUM('EUR', 'USD', name='currency', create_type=False), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('orders')
    op.execute("DROP TYPE orderstatus")
    op.execute("DROP TYPE currency")
