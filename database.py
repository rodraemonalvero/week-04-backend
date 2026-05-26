import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from a local .env file into os.environ.
# This lets us keep secrets (like DATABASE_URL) out of source code.
load_dotenv()

# Read the database connection string from the environment.
# Example value: "postgresql://user:password@localhost:5432/mydb"
DATABASE_URL = os.getenv("DATABASE_URL")

# The engine manages the low-level connection pool to the database.
# It is created once at import time and shared across the application.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory for new Session objects.
# - autocommit=False: changes are staged until we explicitly call commit()
# - autoflush=False:  pending changes are not flushed to the DB on every query
# - bind=engine:      every session created uses our engine's connection pool
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the declarative base class that all ORM models will inherit from.
# SQLAlchemy uses it to collect model metadata so it can create tables, etc.
Base = declarative_base()


def get_db():
    """FastAPI dependency that provides a database session per request.

    Yielding (instead of returning) lets FastAPI run the cleanup code in the
    `finally` block after the request finishes, guaranteeing the session is
    closed even if the endpoint raises an exception.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
