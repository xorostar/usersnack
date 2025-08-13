from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_serializer, Field

class ExtraResponse(BaseModel):
    """Response model for extra/topping information."""
    
    id: UUID = Field(..., description="Unique identifier for the extra")
    name: str = Field(..., description="Name of the extra", min_length=1, max_length=100)
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
