#!/usr/bin/env python3
"""Database initialization script."""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.database import engine, Base
from app.core.config import settings

def init_database():
    """Initialize database tables."""
    print(f"Initializing database: {settings.DATABASE_URL}")
    
    # Import models so they're registered with Base
    from app.schemas.code_analysis import Codebase, CodeFile
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()