from sqlalchemy import Column, String, DateTime, DECIMAL, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
import enum
from ..database.core import Base

class OrderStatus(enum.Enum):
    CREATED = "created"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class Currency(enum.Enum):
    EUR = "EUR"
    USD = "USD"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.CREATED)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(Enum(Currency), nullable=False, default=Currency.EUR)
    customer_name = Column(String, nullable=False)
    customer_address = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Order(status='{self.status.value}', total_amount={self.total_amount}, currency='{self.currency.value}')>"
