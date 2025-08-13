from fastapi.testclient import TestClient
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from src.entities.food_item import FoodItem, FoodCategory
from src.entities.ingredient import Ingredient
from src.entities.food_item_ingredient import FoodItemIngredient

def test_get_food_items(client: TestClient, db_session):
    # Create test ingredients
    ingredient1 = Ingredient(id=uuid.uuid4(), name="tomato")
    ingredient2 = Ingredient(id=uuid.uuid4(), name="cheese")
    db_session.add_all([ingredient1, ingredient2])
    db_session.flush()
    
    # Create test food item
    food_item = FoodItem(
        id=uuid.uuid4(),
        name="Test Pizza",
        category=FoodCategory.PIZZA,
        base_price=Decimal('12.50'),
        image="test.jpg",
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(food_item)
    db_session.flush()
    
    # Create food item ingredient relationships
    food_item_ingredient1 = FoodItemIngredient(
        food_item_id=food_item.id,
        ingredient_id=ingredient1.id
    )
    food_item_ingredient2 = FoodItemIngredient(
        food_item_id=food_item.id,
        ingredient_id=ingredient2.id
    )
    db_session.add_all([food_item_ingredient1, food_item_ingredient2])
    db_session.commit()
    
    # Test GET /food-items/
    response = client.get("/food-items/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Pizza"
    assert data[0]["base_price"] == "12.50"
    assert data[0]["category"] == "pizza"
    assert data[0]["image"] == "test.jpg"
    assert len(data[0]["ingredients"]) == 2
    
    ingredient_names = {ing["name"] for ing in data[0]["ingredients"]}
    assert "tomato" in ingredient_names
    assert "cheese" in ingredient_names

def test_get_food_item_by_id(client: TestClient, db_session):
    # Create test ingredient
    ingredient = Ingredient(id=uuid.uuid4(), name="pepperoni")
    db_session.add(ingredient)
    db_session.flush()
    
    # Create test food item
    food_item = FoodItem(
        id=uuid.uuid4(),
        name="Pepperoni Pizza",
        category=FoodCategory.PIZZA,
        base_price=Decimal('15.00'),
        image="pepperoni.jpg",
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(food_item)
    db_session.flush()
    
    # Create food item ingredient relationship
    food_item_ingredient = FoodItemIngredient(
        food_item_id=food_item.id,
        ingredient_id=ingredient.id
    )
    db_session.add(food_item_ingredient)
    db_session.commit()
    
    # Test GET /food-items/{id}
    response = client.get(f"/food-items/{food_item.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Pepperoni Pizza"
    assert data["base_price"] == "15.00"
    assert data["category"] == "pizza"
    assert data["image"] == "pepperoni.jpg"
    assert len(data["ingredients"]) == 1
    assert data["ingredients"][0]["name"] == "pepperoni"

def test_get_food_item_by_id_not_found(client: TestClient):
    non_existent_id = uuid.uuid4()
    
    response = client.get(f"/food-items/{non_existent_id}")
    assert response.status_code == 404

def test_get_food_items_empty(client: TestClient):
    # Test when no food items exist
    response = client.get("/food-items/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 0
