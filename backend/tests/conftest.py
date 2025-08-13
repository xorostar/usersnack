import pytest
import warnings
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.core import Base
from src.entities.food_item import FoodItem, FoodCategory
from src.entities.ingredient import Ingredient
from src.entities.extra import Extra
from src.entities.order import Order, OrderStatus, Currency
from src.entities.order_item import OrderItem
from src.entities.order_item_extra import OrderItemExtra
from src.entities.food_item_ingredient import FoodItemIngredient


@pytest.fixture(scope="function")
def db_session():
    # Use a unique database URL for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_food_item():
    return FoodItem(
        id=uuid4(),
        name="Test Pizza",
        category=FoodCategory.PIZZA,
        base_price=Decimal('12.50'),
        image="test.jpg",
        created_at=datetime.now(timezone.utc)
    )


@pytest.fixture(scope="function")
def test_ingredient():
    return Ingredient(
        id=uuid4(),
        name="tomato"
    )


@pytest.fixture(scope="function")
def test_extra():
    return Extra(
        id=uuid4(),
        name="ham",
        price=Decimal('2.00')
    )


@pytest.fixture(scope="function")
def client(db_session):
    from src.main import app
    from src.database.core import get_db



    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()



