from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from uuid import UUID

from src.entities.food_item import FoodItem
from src.entities.ingredient import Ingredient
from src.entities.food_item_ingredient import FoodItemIngredient
from src.exceptions import FoodItemNotFoundError

def get_food_items(db: Session):
    """Get all food items with their ingredients."""
    # Query food items and join with ingredients through the relationship table
    food_items = (
        db.query(FoodItem)
        .join(FoodItemIngredient)
        .join(Ingredient)
        .options(joinedload(FoodItem.ingredients))
        .all()
    )
    return food_items

def get_food_item_by_id(db: Session, food_item_id: str):
    """Get a specific food item along with its ingredients."""
    try:
        food_item_uuid = UUID(food_item_id)
    except (ValueError, TypeError):
        raise FoodItemNotFoundError(food_item_id)
    
    food_item = (
        db.query(FoodItem)
        .filter(FoodItem.id == food_item_uuid)
        .join(FoodItemIngredient)
        .join(Ingredient)
        .options(joinedload(FoodItem.ingredients))
        .first()
    )
    
    if not food_item:
        raise FoodItemNotFoundError(food_item_id)
    
    return food_item
