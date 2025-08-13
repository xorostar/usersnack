from fastapi.testclient import TestClient
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from src.entities.food_item import FoodItem, FoodCategory
from src.entities.extra import Extra

def test_create_order_simple(client: TestClient, db_session):
        # Create test food item
        food_item = FoodItem(
            id=uuid.uuid4(),
            name="Test Pizza",
            category=FoodCategory.PIZZA,
            base_price=Decimal('12.00'),
            image="test.jpg",
            created_at=datetime.now(timezone.utc)
        )
        db_session.add(food_item)
        db_session.commit()
        
        # Store the ID before making the request
        food_item_id = str(food_item.id)
        
        # Test POST /orders/
        order_data = {
            "items": [
                {
                    "food_item_id": food_item_id,
                    "quantity": 2,
                    "extra_ids": []
                }
            ],
            "currency": "EUR",
            "customer_name": "Test Customer",
            "customer_address": "123 Test Street, Test City"
        }
        
        response = client.post("/orders/", json=order_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["status"] == "created"
        assert data["currency"] == "EUR"
        assert len(data["items"]) == 1
        assert data["items"][0]["food_item_id"] == food_item_id
        assert data["items"][0]["food_item_name"] == "Test Pizza"
        assert data["items"][0]["quantity"] == 2
        assert data["items"][0]["unit_price"] == "12.00"
        assert data["items"][0]["line_total"] == "24.00"
        assert data["total_amount"] == "24.00"
        assert len(data["items"][0]["extras"]) == 0

def test_create_order_with_extras(client: TestClient, db_session):
    # Create test food item
    food_item = FoodItem(
        id=uuid.uuid4(),
        name="Test Pizza",
        category=FoodCategory.PIZZA,
        base_price=Decimal('10.00'),
        image="test.jpg",
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(food_item)
    
    # Create test extras
    extra1 = Extra(id=uuid.uuid4(), name="ham", price=Decimal('2.00'))
    extra2 = Extra(id=uuid.uuid4(), name="cheese", price=Decimal('1.50'))
    db_session.add_all([extra1, extra2])
    db_session.commit()
    
    # Store the IDs before making the request
    food_item_id = str(food_item.id)
    extra1_id = str(extra1.id)
    extra2_id = str(extra2.id)
    
    # Test POST /orders/
    order_data = {
        "items": [
            {
                "food_item_id": food_item_id,
                "quantity": 1,
                "extra_ids": [extra1_id, extra2_id]
            }
        ],
        "currency": "EUR",
        "customer_name": "Test Customer",
        "customer_address": "123 Test Street, Test City"
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["status"] == "created"
    assert data["currency"] == "EUR"
    assert len(data["items"]) == 1
    assert data["items"][0]["food_item_id"] == food_item_id
    assert data["items"][0]["quantity"] == 1
    assert data["items"][0]["unit_price"] == "13.50"  # 10.00 + 2.00 + 1.50
    assert data["items"][0]["line_total"] == "13.50"
    assert data["total_amount"] == "13.50"
    assert len(data["items"][0]["extras"]) == 2
    
    extra_names = {extra["name"] for extra in data["items"][0]["extras"]}
    assert "ham" in extra_names
    assert "cheese" in extra_names

def test_create_order_multiple_items(client: TestClient, db_session):
    # Create test food items
    food_item1 = FoodItem(
        id=uuid.uuid4(),
        name="Pizza 1",
        category=FoodCategory.PIZZA,
        base_price=Decimal('10.00'),
        image="pizza1.jpg",
        created_at=datetime.now(timezone.utc)
    )
    food_item2 = FoodItem(
        id=uuid.uuid4(),
        name="Pizza 2",
        category=FoodCategory.PIZZA,
        base_price=Decimal('15.00'),
        image="pizza2.jpg",
        created_at=datetime.now(timezone.utc)
    )
    db_session.add_all([food_item1, food_item2])
    
    # Create test extra
    extra = Extra(id=uuid.uuid4(), name="ham", price=Decimal('2.00'))
    db_session.add(extra)
    db_session.commit()
    
    # Store the IDs before making the request
    food_item1_id = str(food_item1.id)
    food_item2_id = str(food_item2.id)
    extra_id = str(extra.id)
    
    # Test POST /orders/
    order_data = {
        "items": [
            {
                "food_item_id": food_item1_id,
                "quantity": 2,
                "extra_ids": [extra_id]
            },
            {
                "food_item_id": food_item2_id,
                "quantity": 1,
                "extra_ids": []
            }
        ],
        "currency": "EUR",
        "customer_name": "Test Customer",
        "customer_address": "123 Test Street, Test City"
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["status"] == "created"
    assert data["currency"] == "EUR"
    assert len(data["items"]) == 2
    
    # Check first item (Pizza 1 with ham, quantity 2)
    item1 = data["items"][0]
    assert item1["food_item_id"] == food_item1_id
    assert item1["quantity"] == 2
    assert item1["unit_price"] == "12.00"  # 10.00 + 2.00
    assert item1["line_total"] == "24.00"  # 12.00 * 2
    
    # Check second item (Pizza 2, quantity 1)
    item2 = data["items"][1]
    assert item2["food_item_id"] == food_item2_id
    assert item2["quantity"] == 1
    assert item2["unit_price"] == "15.00"
    assert item2["line_total"] == "15.00"
    
    # Check total
    assert data["total_amount"] == "39.00"  # 24.00 + 15.00

def test_create_order_food_item_not_found(client: TestClient):
    non_existent_food_item_id = uuid.uuid4()
    
    order_data = {
        "items": [
            {
                "food_item_id": str(non_existent_food_item_id),
                "quantity": 1,
                "extra_ids": []
            }
        ],
        "currency": "EUR",
        "customer_name": "Test Customer",
        "customer_address": "123 Test Street, Test City"
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 404
    assert f"Food items not found: {non_existent_food_item_id}" in response.json()["detail"]

def test_create_order_extra_not_found(client: TestClient, db_session):
    # Create test food item
    food_item = FoodItem(
        id=uuid.uuid4(),
        name="Test Pizza",
        category=FoodCategory.PIZZA,
        base_price=Decimal('10.00'),
        image="test.jpg",
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(food_item)
    db_session.commit()
    
    non_existent_extra_id = uuid.uuid4()
    
    order_data = {
        "items": [
            {
                "food_item_id": str(food_item.id),
                "quantity": 1,
                "extra_ids": [str(non_existent_extra_id)]
            }
        ],
        "currency": "EUR",
        "customer_name": "Test Customer",
        "customer_address": "123 Test Street, Test City"
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 404
    assert f"Extras not found: {non_existent_extra_id}" in response.json()["detail"]

def test_create_order_invalid_quantity(client: TestClient, db_session):
    # Create test food item
    food_item = FoodItem(
        id=uuid.uuid4(),
        name="Test Pizza",
        category=FoodCategory.PIZZA,
        base_price=Decimal('10.00'),
        image="test.jpg",
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(food_item)
    db_session.commit()
    
    # Test with quantity 0
    order_data = {
        "items": [
            {
                "food_item_id": str(food_item.id),
                "quantity": 0,
                "extra_ids": []
            }
        ],
        "currency": "EUR",
        "customer_name": "Test Customer",
        "customer_address": "123 Test Street, Test City"
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 422  # Validation error

def test_create_order_invalid_currency(client: TestClient, db_session):
    # Create test food item
    food_item = FoodItem(
        id=uuid.uuid4(),
        name="Test Pizza",
        category=FoodCategory.PIZZA,
        base_price=Decimal('10.00'),
        image="test.jpg",
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(food_item)
    db_session.commit()
    
    # Test with invalid currency
    order_data = {
        "items": [
            {
                "food_item_id": str(food_item.id),
                "quantity": 1,
                "extra_ids": []
            }
        ],
        "currency": "INVALID",
        "customer_name": "Test Customer",
        "customer_address": "123 Test Street, Test City"
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 422  # Validation error
