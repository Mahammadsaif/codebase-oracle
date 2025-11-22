from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings using Pydantic for validation."""
    
    # Database
    DATABASE_URL: str
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Codebase Oracle"
    
    # Environment
    ENVIRONMENT: str = "development"  # development, testing, production
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()