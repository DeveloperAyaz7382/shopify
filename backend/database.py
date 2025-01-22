from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from contextlib import contextmanager

# Replace with your PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:root@localhost/shopify_clone"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Session maker to interact with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class to define models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
