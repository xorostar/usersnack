import pytest
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from src.orders import service as orders_service
from src.orders.models import OrderCreate, OrderItemCreate
from src.entities.food_item import FoodItem, FoodCategory
from src.entities.extra import Extra
from src.entities.order import Currency
from fastapi import HTTPException

class TestOrdersService:
    def test_create_order_simple(self, db_session):
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
        
        # Create order request
        order_create = OrderCreate(
            items=[
                OrderItemCreate(
                    food_item_id=food_item.id,
                    quantity=2,
                    extra_ids=[]
                )
            ],
            currency=Currency.EUR,
            customer_name="Test Customer",
            customer_address="123 Test Street, Test City"
        )
        
        # Test order creation
        result = orders_service.create_order(db_session, order_create)
        
        assert result.status == "created"
        assert result.currency == "EUR"
        assert len(result.items) == 1
        assert result.items[0].food_item_id == food_item.id
        assert result.items[0].food_item_name == "Test Pizza"
        assert result.items[0].quantity == 2
        assert result.items[0].unit_price == Decimal('12.00')
        assert result.items[0].line_total == Decimal('24.00')
        assert result.total_amount == Decimal('24.00')
        assert len(result.items[0].extras) == 0

    def test_create_order_with_extras(self, db_session):
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
        
        # Create order request
        order_create = OrderCreate(
            items=[
                OrderItemCreate(
                    food_item_id=food_item.id,
                    quantity=1,
                    extra_ids=[extra1.id, extra2.id]
                )
            ],
            currency=Currency.EUR,
            customer_name="Test Customer",
            customer_address="123 Test Street, Test City"
        )
        
        # Test order creation
        result = orders_service.create_order(db_session, order_create)
        
        assert result.status == "created"
        assert result.currency == "EUR"
        assert len(result.items) == 1
        assert result.items[0].food_item_id == food_item.id
        assert result.items[0].quantity == 1
        assert result.items[0].unit_price == Decimal('13.50')  # 10.00 + 2.00 + 1.50
        assert result.items[0].line_total == Decimal('13.50')
        assert result.total_amount == Decimal('13.50')
        assert len(result.items[0].extras) == 2
        extra_names = {extra.name for extra in result.items[0].extras}
        assert "ham" in extra_names
        assert "cheese" in extra_names

    def test_create_order_multiple_items(self, db_session):
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
        
        # Create order request
        order_create = OrderCreate(
            items=[
                OrderItemCreate(
                    food_item_id=food_item1.id,
                    quantity=2,
                    extra_ids=[extra.id]
                ),
                OrderItemCreate(
                    food_item_id=food_item2.id,
                    quantity=1,
                    extra_ids=[]
                )
            ],
            currency=Currency.EUR,
            customer_name="Test Customer",
            customer_address="123 Test Street, Test City"
        )
        
        # Test order creation
        result = orders_service.create_order(db_session, order_create)
        
        assert result.status == "created"
        assert result.currency == "EUR"
        assert len(result.items) == 2
        
        # Check first item (Pizza 1 with ham, quantity 2)
        item1 = result.items[0]
        assert item1.food_item_id == food_item1.id
        assert item1.quantity == 2
        assert item1.unit_price == Decimal('12.00')  # 10.00 + 2.00
        assert item1.line_total == Decimal('24.00')  # 12.00 * 2
        
        # Check second item (Pizza 2, quantity 1)
        item2 = result.items[1]
        assert item2.food_item_id == food_item2.id
        assert item2.quantity == 1
        assert item2.unit_price == Decimal('15.00')
        assert item2.line_total == Decimal('15.00')
        
        # Check total
        assert result.total_amount == Decimal('39.00')  # 24.00 + 15.00

    def test_create_order_food_item_not_found(self, db_session):
        non_existent_food_item_id = uuid.uuid4()
        
        order_create = OrderCreate(
            items=[
                OrderItemCreate(
                    food_item_id=non_existent_food_item_id,
                    quantity=1,
                    extra_ids=[]
                )
            ],
            currency=Currency.EUR,
            customer_name="Test Customer",
            customer_address="123 Test Street, Test City"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            orders_service.create_order(db_session, order_create)
        
        assert exc_info.value.status_code == 404
        assert f"Food items not found: {non_existent_food_item_id}" in str(exc_info.value.detail)

    def test_create_order_extra_not_found(self, db_session):
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
        
        order_create = OrderCreate(
            items=[
                OrderItemCreate(
                    food_item_id=food_item.id,
                    quantity=1,
                    extra_ids=[non_existent_extra_id]
                )
            ],
            currency=Currency.EUR,
            customer_name="Test Customer",
            customer_address="123 Test Street, Test City"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            orders_service.create_order(db_session, order_create)
        
        assert exc_info.value.status_code == 404
        assert f"Extras not found: {non_existent_extra_id}" in str(exc_info.value.detail)
