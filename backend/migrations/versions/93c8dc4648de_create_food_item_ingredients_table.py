"""create food_item_ingredients table

Revision ID: 93c8dc4648de
Revises: 6f94f08c70d5
Create Date: 2025-08-12 23:39:47.483935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '93c8dc4648de'
down_revision: Union[str, Sequence[str], None] = '6f94f08c70d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('food_item_ingredients',
        sa.Column('food_item_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ingredient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['food_item_id'], ['food_items.id'], ),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
        sa.PrimaryKeyConstraint('food_item_id', 'ingredient_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('food_item_ingredients')
