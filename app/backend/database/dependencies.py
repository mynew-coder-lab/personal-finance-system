"""
FastAPI database dependencies.

Provides get_db() — a dependency that yields a SQLAlchemy session
per request and ensures it is closed afterward.
"""

from typing import Generator

from sqlalchemy.orm import Session

from app.backend.database.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a database session per request, auto-close on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
