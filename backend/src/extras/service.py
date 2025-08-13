from sqlalchemy.orm import Session
from src.entities.extra import Extra

def get_extras(db: Session):
    """Get all available extras."""
    return db.query(Extra).all()
