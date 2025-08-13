from sqlalchemy import Column, String, DateTime, DECIMAL, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
import enum
from ..database.core import Base

class FoodCategory(enum.Enum):
    PIZZA = "pizza"
    BURGER = "burger"
    SALAD = "salad"
    DESSERT = "dessert"
    DRINK = "drink"
    SIDE = "side"

class FoodItem(Base):
    __tablename__ = 'food_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category = Column(Enum(FoodCategory), nullable=False)
    base_price = Column(DECIMAL(10, 2), nullable=False)
    image = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    ingredients = relationship("Ingredient", secondary="food_item_ingredients", back_populates="food_items")

    def __repr__(self):
        return f"<FoodItem(name='{self.name}', category='{self.category.value}', base_price={self.base_price})>"
