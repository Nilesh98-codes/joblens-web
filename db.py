"""
db.py — Database engine factory for JobLens.

Provides a shared SQLAlchemy engine, lazily initialized from DATABASE_URL.
Tests override this via environment variable TEST_DATABASE_URL.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

_engine = None


def get_engine():
    """Return the shared SQLAlchemy engine (created once, reused)."""
    global _engine
    if _engine is None:
        url = os.environ.get("DATABASE_URL")
        if not url:
            raise RuntimeError("DATABASE_URL environment variable is not set.")
        _engine = create_engine(url)
    return _engine


def reset_engine():
    """Force recreation of the engine (used by tests to switch databases)."""
    global _engine
    if _engine is not None:
        _engine.dispose()
    _engine = None
