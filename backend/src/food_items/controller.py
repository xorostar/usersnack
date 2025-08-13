from typing import List
from fastapi import APIRouter, Depends

from src.database.core import DbSession
from . import models
from . import service

router = APIRouter(
    prefix="/food-items",
    tags=["Food Items"]
)

@router.get("/", response_model=List[models.FoodItemResponse], operation_id="get_food_items")
def get_food_items(db: DbSession):
    """Get all food items with their ingredients."""
    return service.get_food_items(db)

@router.get("/{food_item_id}", response_model=models.FoodItemResponse, operation_id="get_food_item")
def get_food_item(food_item_id: str, db: DbSession):
    """Get a specific food item with its ingredients."""
    return service.get_food_item_by_id(db, food_item_id)
