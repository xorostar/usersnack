import pytest
from uuid import uuid4
from decimal import Decimal
from src.extras import service as extras_service
from src.entities.extra import Extra

class TestExtrasService:
    def test_get_extras(self, db_session):
        # Create test extras
        extra1 = Extra(id=uuid4(), name="ham", price=Decimal('2.00'))
        extra2 = Extra(id=uuid4(), name="cheese", price=Decimal('1.50'))
        extra3 = Extra(id=uuid4(), name="mushrooms", price=Decimal('1.20'))
        
        db_session.add_all([extra1, extra2, extra3])
        db_session.commit()
        
        # Test getting all extras
        extras = extras_service.get_extras(db_session)
        assert len(extras) == 3
        
        # Check that all extras are returned
        extra_names = {extra.name for extra in extras}
        assert "ham" in extra_names
        assert "cheese" in extra_names
        assert "mushrooms" in extra_names
        
        # Check prices
        for extra in extras:
            if extra.name == "ham":
                assert extra.price == Decimal('2.00')
            elif extra.name == "cheese":
                assert extra.price == Decimal('1.50')
            elif extra.name == "mushrooms":
                assert extra.price == Decimal('1.20')

    def test_get_extras_empty(self, db_session):
        # Test getting extras when none exist
        extras = extras_service.get_extras(db_session)
        assert len(extras) == 0
