from fastapi import HTTPException

class FoodItemError(HTTPException):
    """Base exception for food item-related errors"""
    pass

class FoodItemNotFoundError(FoodItemError):
    def __init__(self, food_item_id=None):
        message = "Food item not found" if food_item_id is None else f"Food item with id {food_item_id} not found"
        super().__init__(status_code=404, detail=message)
