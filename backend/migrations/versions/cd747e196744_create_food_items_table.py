"""create food_items table

Revision ID: cd747e196744
Revises: 833236fe652e
Create Date: 2025-08-12 23:39:47.483935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cd747e196744'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE foodcategory AS ENUM ('PIZZA', 'BURGER', 'SALAD', 'DESSERT', 'DRINK', 'SIDE')")
    
    op.create_table('food_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', postgresql.ENUM('PIZZA', 'BURGER', 'SALAD', 'DESSERT', 'DRINK', 'SIDE', name='foodcategory', create_type=False), nullable=False),
        sa.Column('base_price', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('image', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('food_items')
    op.execute("DROP TYPE foodcategory")
