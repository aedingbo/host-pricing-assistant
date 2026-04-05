"""
Database configuration for the Host Pricing Assistant backend.

This file defines the SQLite database connection and provides
shared database utilities for the application.
"""

from sqlmodel import SQLModel, create_engine


# Define the SQLite database file path.
# SQLite stores the database in a local file instead of requiring
# a separate database server.
DATABASE_URL = "sqlite:///host_pricing_assistant.db"


# Create the SQLModel engine.
# The engine is the main connection interface the application uses
# to talk to the database.
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """
    Create all database tables defined by SQLModel models.

    This function should be called during application startup so
    the required tables exist before the app begins handling requests.
    """
    SQLModel.metadata.create_all(engine)