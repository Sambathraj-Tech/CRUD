# app/database.py
# ---------------------------------------------------------------
# Database engine creation and session management with SQLAlchemy.
# FastAPI uses dependency injection — get_db() is injected into
# route handlers so each request gets its own DB session.
# ---------------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings
from app.logger import logger


# --- Engine ---
# connect_args is only needed for SQLite (not PostgreSQL).
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)
engine = create_engine(
    settings.DATABASE_URL,
    # pool_pre_ping=True  → detects stale connections automatically
    pool_pre_ping=True,
    echo=settings.DEBUG,  # Log all SQL statements in debug mode
    connect_args=connect_args,
)

# --- Session factory ---
# autocommit=False → we control transactions manually
# autoflush=False  → prevents premature writes before we're ready
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Base class for all ORM models ---
class Base(DeclarativeBase):
    pass


# --- Dependency for FastAPI route handlers ---
def get_db():
    """
    Yield a database session for a single request, then close it.

    Usage in routes:
        def my_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        logger.debug("Opening new database session")
        yield db
    except Exception as exc:
        logger.error(f"Database session error: {exc}")
        db.rollback()
        raise
    finally:
        logger.debug("Closing database session")
        db.close()