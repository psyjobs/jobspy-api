"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from app.config import settings

logger = logging.getLogger(__name__)

# Get database URL from settings or use SQLite in-memory if not configured
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL or "sqlite:///:memory:"

# Only create engine if a database URL is provided
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL != "sqlite:///:memory:":
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    logger.warning("No DATABASE_URL configured, database functionality will be limited")
    engine = None
    SessionLocal = None

Base = declarative_base()

def get_db():
    """Get a database session."""
    if SessionLocal is None:
        raise RuntimeError("Database not configured. Set DATABASE_URL in environment.")
        
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
