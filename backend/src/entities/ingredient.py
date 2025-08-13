from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from ..database.core import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)

    # Relationships
    food_items = relationship("FoodItem", secondary="food_item_ingredients", back_populates="ingredients")

    def __repr__(self):
        return f"<Ingredient(name='{self.name}')>"
