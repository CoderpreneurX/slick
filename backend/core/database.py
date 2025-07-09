"""
This module contains the database configuration and dependencies.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from core.config import get_settings

settings = get_settings()

# Get the database URL from application settings
DATABASE_URL = settings.DATABASE_URL

# Connect args needed only for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if str(DATABASE_URL).startswith("sqlite") else {}
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to be used in routes
def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.

    Yields:
        Session: A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
