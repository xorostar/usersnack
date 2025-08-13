from fastapi import FastAPI
from src.food_items.controller import router as food_items_router
from src.extras.controller import router as extras_router
from src.orders.controller import router as orders_router

def register_routes(app: FastAPI):
    app.include_router(food_items_router)
    app.include_router(extras_router)
    app.include_router(orders_router)