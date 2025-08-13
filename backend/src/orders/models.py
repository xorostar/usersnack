from uuid import UUID
from decimal import Decimal
from typing import List
from pydantic import BaseModel, ConfigDict, Field, field_validator, field_serializer
from src.entities.order import Currency

class OrderItemCreate(BaseModel):
    """Request model for creating an order item."""
    
    food_item_id: UUID = Field(..., description="Unique identifier of the food item")
    quantity: int = Field(..., description="Quantity of the food item", ge=1, le=100)
    extra_ids: List[UUID] = Field(default_factory=list, description="List of extra IDs to add to this item")
    
    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v < 1:
            raise ValueError('quantity must be greater than or equal to 1')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "food_item_id": "e5883f82-5a85-4d3b-8820-e88cea7fd0df",
                "quantity": 2,
                "extra_ids": ["a863e8c9-1d88-4a68-a245-13fa871d49d4", "90924490-29af-4edd-89e5-fc8e58f520dd"]
            }
        }
    )

class OrderCreate(BaseModel):
    """Request model for creating a new order."""
    
    items: List[OrderItemCreate] = Field(..., description="List of order items", min_length=1)
    currency: Currency = Field(..., description="Currency for the order")
    customer_name: str = Field(..., description="Customer's full name", min_length=1, max_length=200)
    customer_address: str = Field(..., description="Customer's delivery address", min_length=1, max_length=500)
    
    @field_validator('items')
    @classmethod
    def validate_items_not_empty(cls, v):
        if not v:
            raise ValueError('Order must contain at least one item')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "food_item_id": "e5883f82-5a85-4d3b-8820-e88cea7fd0df",
                        "quantity": 2,
                        "extra_ids": ["a863e8c9-1d88-4a68-a245-13fa871d49d4"]
                    }
                ],
                "currency": "EUR",
                "customer_name": "John Doe",
                "customer_address": "123 Main St, City, Country"
            }
        }
    )

class ExtraInResponse(BaseModel):
    """Response model for extra information within an order."""
    
    id: UUID = Field(..., description="Unique identifier for the extra")
    name: str = Field(..., description="Name of the extra")
    price: Decimal = Field(..., description="Price of the extra", ge=Decimal('0'))
    
    @field_serializer('price')
    def serialize_price(self, price: Decimal) -> str:
        return str(price)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "a863e8c9-1d88-4a68-a245-13fa871d49d4",
                "name": "Extra Cheese",
                "price": "2.50"
            }
        }
    )

class OrderItemResponse(BaseModel):
    """Response model for order item information."""
    
    food_item_id: UUID = Field(..., description="Unique identifier of the food item")
    food_item_name: str = Field(..., description="Name of the food item")
    quantity: int = Field(..., description="Quantity ordered", ge=1)
    unit_price: Decimal = Field(..., description="Unit price of the food item", ge=Decimal('0'))
    extras: List[ExtraInResponse] = Field(..., description="List of extras added to this item")
    line_total: Decimal = Field(..., description="Total price for this line item", ge=Decimal('0'))
    
    @field_serializer('unit_price')
    def serialize_unit_price(self, unit_price: Decimal) -> str:
        return str(unit_price)
    
    @field_serializer('line_total')
    def serialize_line_total(self, line_total: Decimal) -> str:
        return str(line_total)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "food_item_id": "e5883f82-5a85-4d3b-8820-e88cea7fd0df",
                "food_item_name": "Cheese & Tomato Pizza",
                "quantity": 2,
                "unit_price": "11.90",
                "extras": [
                    {
                        "id": "a863e8c9-1d88-4a68-a245-13fa871d49d4",
                        "name": "Extra Cheese",
                        "price": "2.50"
                    }
                ],
                "line_total": "28.80"
            }
        }
    )

class OrderResponse(BaseModel):
    """Response model for order information."""
    
    id: UUID = Field(..., description="Unique identifier for the order")
    status: str = Field(..., description="Current status of the order")
    currency: str = Field(..., description="Currency used for the order")
    customer_name: str = Field(..., description="Customer's full name")
    customer_address: str = Field(..., description="Customer's delivery address")
    items: List[OrderItemResponse] = Field(..., description="List of order items")
    total_amount: Decimal = Field(..., description="Total amount for the entire order", ge=Decimal('0'))
    created_at: str = Field(..., description="ISO timestamp when the order was created")
    
    @field_serializer('total_amount')
    def serialize_total_amount(self, total_amount: Decimal) -> str:
        return str(total_amount)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "status": "created",
                "currency": "EUR",
                "customer_name": "John Doe",
                "customer_address": "123 Main St, City, Country",
                "items": [
                    {
                        "food_item_id": "e5883f82-5a85-4d3b-8820-e88cea7fd0df",
                        "food_item_name": "Cheese & Tomato Pizza",
                        "quantity": 2,
                        "unit_price": "11.90",
                        "extras": [
                            {
                                "id": "a863e8c9-1d88-4a68-a245-13fa871d49d4",
                                "name": "Extra Cheese",
                                "price": "2.50"
                            }
                        ],
                        "line_total": "28.80"
                    }
                ],
                "total_amount": "28.80",
                "created_at": "2025-01-15T10:30:00Z"
            }
        }
    )
