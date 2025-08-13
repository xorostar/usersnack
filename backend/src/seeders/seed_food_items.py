#!/usr/bin/env python3
"""
Seeder script to load food items and extras data from data.json into the database.
"""

import os
import json
from decimal import Decimal
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.core import Base
from src.entities.food_item import FoodItem, FoodCategory
from src.entities.ingredient import Ingredient
from src.entities.food_item_ingredient import FoodItemIngredient
from src.entities.extra import Extra
from src.entities.order_item_extra import OrderItemExtra
from src.entities.order import Order
from src.entities.order_item import OrderItem

def parse_data_file(file_path: str) -> tuple[list, list]:
    """
    Parse the data.json file and extract pizzas and extras.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    pizzas = []
    for pizza in data.get("Pizza", []):
        pizzas.append({
            "name": pizza["name"],
            "price": Decimal(str(pizza["price"])),
            "image": pizza.get("img"),
            "ingredients": pizza.get("ingredients", []),
        })
    extras = []
    for extra in data.get("Extras", []):
        extras.append({
            "name": extra["name"],
            "price": Decimal(str(extra["price"]))
        })
    return pizzas, extras


def clear_database(db):
    """
    Delete all data from the relevant tables before seeding.
    """
    print("Clearing database tables...")
    
    db.query(OrderItemExtra).delete()
    db.query(OrderItem).delete()
    db.query(Order).delete()
    db.query(FoodItemIngredient).delete()
    db.query(Extra).delete()
    db.query(FoodItem).delete()
    db.query(Ingredient).delete()
    db.commit()


def seed_ingredients(db, pizzas: list) -> dict:
    """
    Create ingredients from pizza data and return a mapping of ingredient names to IDs.
    """
    ingredient_map = {}
    all_ingredients = set()
    for pizza in pizzas:
        all_ingredients.update(pizza['ingredients'])
    for ingredient_name in sorted(all_ingredients):
        ingredient = Ingredient(
            id=uuid4(),
            name=ingredient_name
        )
        db.add(ingredient)
        db.flush()
        ingredient_map[ingredient_name] = ingredient.id
    db.commit()
    return ingredient_map


def seed_food_items(db, pizzas: list, ingredient_map: dict):
    """
    Create food items and their ingredient relationships.
    """
    for pizza_data in pizzas:
        food_item = FoodItem(
            id=uuid4(),
            name=pizza_data['name'],
            category=FoodCategory.PIZZA,
            base_price=pizza_data['price'],
            image=pizza_data['image'],
            created_at=datetime.now(timezone.utc)
        )
        db.add(food_item)
        db.flush()
        for ingredient_name in pizza_data['ingredients']:
            if ingredient_name in ingredient_map:
                food_item_ingredient = FoodItemIngredient(
                    food_item_id=food_item.id,
                    ingredient_id=ingredient_map[ingredient_name]
                )
                db.add(food_item_ingredient)
    db.commit()


def seed_extras(db, extras: list):
    """
    Create extras in the database.
    """
    for extra_data in extras:
        extra = Extra(
            id=uuid4(),
            name=extra_data['name'],
            price=extra_data['price']
        )
        db.add(extra)
    db.commit()


if __name__ == "__main__":
    print("Starting data seeding...")

    # Use data.json in the project root
    data_file_path = os.path.join(os.path.dirname(__file__), 'data.json')

    if not os.path.exists(data_file_path):
        print(f"Error: data.json not found at {data_file_path}")
        exit(1)

    try:
        print("Parsing data.json...")
        pizzas, extras = parse_data_file(data_file_path)

        print(f"Found {len(pizzas)} pizzas and {len(extras)} extras")

        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cleanfastapi")
        engine = create_engine(database_url)
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        try:
            clear_database(db)

            print("Seeding ingredients...")
            ingredient_map = seed_ingredients(db, pizzas)

            print("Seeding food items...")
            seed_food_items(db, pizzas, ingredient_map)

            print("Seeding extras...")
            seed_extras(db, extras)

            print("Data seeding completed successfully!")

        finally:
            db.close()

    except Exception as e:
        print(f"Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
