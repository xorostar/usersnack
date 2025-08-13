from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_serializer, Field
from typing import List, Optional
from datetime import datetime

class IngredientResponse(BaseModel):
    """Response model for ingredient information."""
    
    id: UUID = Field(..., description="Unique identifier for the ingredient")
    name: str = Field(..., description="Name of the ingredient", min_length=1, max_length=100)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "3e1a5dea-b214-49a5-94aa-4650343d2bd0",
                "name": "tomato"
            }
        }
    )

class FoodItemResponse(BaseModel):
    """Response model for food item information."""
    
    id: UUID = Field(..., description="Unique identifier for the food item")
    name: str = Field(..., description="Name of the food item", min_length=1, max_length=200)
    category: str = Field(..., description="Category of the food item", min_length=1, max_length=50)
    base_price: Decimal = Field(..., description="Base price of the food item", ge=Decimal('0'))
    image: Optional[str] = Field(None, description="URL to the food item image")
    created_at: datetime = Field(..., description="Timestamp when the food item was created")
    ingredients: List[IngredientResponse] = Field(..., description="List of ingredients in the food item")
    
    @field_serializer('base_price')
    def serialize_base_price(self, base_price: Decimal) -> str:
        return str(base_price)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "e5883f82-5a85-4d3b-8820-e88cea7fd0df",
                "name": "Cheese & Tomato Pizza",
                "category": "pizza",
                "base_price": "11.90",
                "image": "https://example.com/pizza-image.jpg",
                "created_at": "2025-01-15T10:30:00Z",
                "ingredients": [
                    {
                        "id": "3e1a5dea-b214-49a5-94aa-4650343d2bd0",
                        "name": "tomato"
                    },
                    {
                        "id": "9c7da8d8-5212-4bd4-9dda-7b04be188e02",
                        "name": "cheese"
                    }
                ]
            }
        }
    )
