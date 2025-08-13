from fastapi.testclient import TestClient
import uuid
from decimal import Decimal
from src.entities.extra import Extra

def test_get_extras(client: TestClient, db_session):
    # Create test extras
    extra1 = Extra(id=uuid.uuid4(), name="ham", price=Decimal('2.00'))
    extra2 = Extra(id=uuid.uuid4(), name="cheese", price=Decimal('1.50'))
    extra3 = Extra(id=uuid.uuid4(), name="mushrooms", price=Decimal('1.20'))
    
    db_session.add_all([extra1, extra2, extra3])
    db_session.commit()
    
    # Test GET /extras/
    response = client.get("/extras/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3
    
    # Check that all extras are returned
    extra_names = {extra["name"] for extra in data}
    assert "ham" in extra_names
    assert "cheese" in extra_names
    assert "mushrooms" in extra_names
    
    # Check prices
    for extra in data:
        if extra["name"] == "ham":
            assert extra["price"] == "2.00"
        elif extra["name"] == "cheese":
            assert extra["price"] == "1.50"
        elif extra["name"] == "mushrooms":
            assert extra["price"] == "1.20"

def test_get_extras_empty(client: TestClient):
    # Test when no extras exist
    response = client.get("/extras/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 0
