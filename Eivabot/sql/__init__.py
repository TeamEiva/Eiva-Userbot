import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from Eivabot.config import Config


def start() -> scoped_session:
    # Keep the built-in database features usable on a fresh local install.
    # Operators can set DATABASE_URL to PostgreSQL for persistent deployments.
    database_url = Config.DB_URI or "sqlite:///eiva.db"
    engine = create_engine(database_url)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
try:
    SESSION = start()
except Exception:
    import logging
    logging.getLogger(__name__).exception("Database initialization failed")
