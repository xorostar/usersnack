from .database.core import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .entities.food_item import FoodItem, FoodCategory 
from .entities.ingredient import Ingredient
from .entities.food_item_ingredient import FoodItemIngredient
from .entities.extra import Extra
from .entities.order import Order
from .entities.order_item import OrderItem
from .entities.order_item_extra import OrderItemExtra
from .api import register_routes
from .logging import configure_logging, LogLevels
from .config import settings

configure_logging(LogLevels.info)

app = FastAPI(
    title="Usersnack API",
    description="""Usersnack Food Ordering API""",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),  # Frontend URLs from environment
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


register_routes(app)
