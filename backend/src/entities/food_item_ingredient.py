from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..database.core import Base

class FoodItemIngredient(Base):
    __tablename__ = 'food_item_ingredients'

    food_item_id = Column(UUID(as_uuid=True), ForeignKey('food_items.id'), primary_key=True)
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey('ingredients.id'), primary_key=True)

    def __repr__(self):
        return f"<FoodItemIngredient(food_item_id='{self.food_item_id}', ingredient_id='{self.ingredient_id}')>"
