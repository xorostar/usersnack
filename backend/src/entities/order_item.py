from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    food_item_id = Column(UUID(as_uuid=True), ForeignKey('food_items.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(DECIMAL(10, 2), nullable=False)

    def __repr__(self):
        return f"<OrderItem(order_id='{self.order_id}', food_item_id='{self.food_item_id}', quantity={self.quantity}, unit_price={self.unit_price})>"
