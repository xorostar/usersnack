from sqlalchemy import Column, String, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..database.core import Base

class Extra(Base):
    __tablename__ = 'extras'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    price = Column(DECIMAL(10, 2), nullable=False)

    def __repr__(self):
        return f"<Extra(name='{self.name}', price={self.price})>"
