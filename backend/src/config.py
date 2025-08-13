import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/usersnack")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    
    @classmethod
    def get_allowed_origins(cls) -> List[str]:
        """Get allowed origins for CORS, with fallback to default values."""
        return cls.ALLOWED_ORIGINS

settings = Settings()
