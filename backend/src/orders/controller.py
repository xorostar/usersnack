from fastapi import APIRouter, status, Depends

from src.database.core import DbSession
from . import models
from . import service

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model=models.OrderResponse, status_code=status.HTTP_201_CREATED, operation_id="create_order")
def create_order(order: models.OrderCreate, db: DbSession):
    """Create a new order."""
    return service.create_order(db, order)
