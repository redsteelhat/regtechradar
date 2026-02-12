"""SQLAlchemy sync engine and session for collector (raw storage, processing)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

try:
    from src.config import settings
    _database_url = settings.database_url
except Exception:
    import os
    _database_url = os.getenv("DATABASE_URL", "postgresql://regtech:regtech@localhost:5432/regtechradar")

if _database_url.startswith("postgresql://") and "postgresql+psycopg" not in _database_url:
    _database_url = _database_url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(_database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)


def get_session() -> Session:
    """Return a new DB session (caller should close or use as context)."""
    return SessionLocal()
