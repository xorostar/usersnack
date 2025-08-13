import pytest
from uuid import uuid4
from decimal import Decimal
from datetime import datetime, timezone
from src.food_items import service as food_items_service
from src.entities.food_item import FoodItem, FoodCategory
from src.entities.ingredient import Ingredient
from src.entities.food_item_ingredient import FoodItemIngredient
from src.exceptions import FoodItemNotFoundError

class TestFoodItemsService:
    def test_get_food_items(self, db_session):
        # Create test ingredients
        ingredient1 = Ingredient(id=uuid4(), name="tomato")
        ingredient2 = Ingredient(id=uuid4(), name="cheese")
        db_session.add_all([ingredient1, ingredient2])
        db_session.flush()
        
        # Create test food item
        food_item = FoodItem(
            id=uuid4(),
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
        
        # Test getting all food items
        food_items = food_items_service.get_food_items(db_session)
        assert len(food_items) == 1
        assert food_items[0].name == "Test Pizza"
        assert food_items[0].base_price == Decimal('12.50')
        assert len(food_items[0].ingredients) == 2
        ingredient_names = {ing.name for ing in food_items[0].ingredients}
        assert "tomato" in ingredient_names
        assert "cheese" in ingredient_names

    def test_get_food_item_by_id(self, db_session):
        # Create test ingredient
        ingredient = Ingredient(id=uuid4(), name="pepperoni")
        db_session.add(ingredient)
        db_session.flush()
        
        # Create test food item
        food_item = FoodItem(
            id=uuid4(),
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
        
        # Test getting food item by ID
        result = food_items_service.get_food_item_by_id(db_session, str(food_item.id))
        assert result.name == "Pepperoni Pizza"
        assert result.base_price == Decimal('15.00')
        assert len(result.ingredients) == 1
        assert result.ingredients[0].name == "pepperoni"

    def test_get_food_item_by_id_not_found(self, db_session):
        non_existent_id = uuid4()
        
        with pytest.raises(FoodItemNotFoundError):
            food_items_service.get_food_item_by_id(db_session, str(non_existent_id))
