from sqlalchemy import Column, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from ..database.core import Base

class OrderItemExtra(Base):
    __tablename__ = 'order_item_extras'

    order_item_id = Column(UUID(as_uuid=True), ForeignKey('order_items.id'), primary_key=True)
    extra_id = Column(UUID(as_uuid=True), ForeignKey('extras.id'), primary_key=True)
    extra_price = Column(DECIMAL(10, 2), nullable=False)

    def __repr__(self):
        return f"<OrderItemExtra(order_item_id='{self.order_item_id}', extra_id='{self.extra_id}', extra_price={self.extra_price})>"
