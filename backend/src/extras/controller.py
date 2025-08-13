from typing import List
from fastapi import APIRouter, Depends

from src.database.core import DbSession
from . import models
from . import service

router = APIRouter(
    prefix="/extras",
    tags=["Extras"]
)

@router.get("/", response_model=List[models.ExtraResponse], operation_id="get_extras")
def get_extras(db: DbSession):
    """Get all available extras."""
    return service.get_extras(db)
