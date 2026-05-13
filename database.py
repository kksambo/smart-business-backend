"""
Database configuration and session management
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
import os

# SQLite database URL
DATABASE_URL = "sqlite:///./business_app.db"

# Create engine with SQLite-specific configuration
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Create SessionLocal for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    _migrate_legacy_location_table()


def _migrate_legacy_location_table():
    """Migrate legacy 'locations' rows into the new 'business_locations' table."""
    with engine.begin() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='locations'"))
        has_legacy = result.scalar() is not None

        result_new = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='business_locations'"))
        has_new = result_new.scalar() is not None

        if has_legacy and has_new:
            conn.execute(text(
                "INSERT OR IGNORE INTO business_locations "
                "(id, owner_id, name, latitude, longitude, region, total_sales, description, created_at) "
                "SELECT id, owner_id, name, latitude, longitude, region, total_sales, description, created_at FROM locations"
            ))
            conn.execute(text("DROP TABLE IF EXISTS locations"))


def drop_tables():
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine)
