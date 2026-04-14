# app/main.py
# ---------------------------------------------------------------
# FastAPI application factory.
# This is the entry point for the entire application.
# ---------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.controllers.task_controller import router as task_router
from app.controllers.user_controller import router as user_router
from app.database import Base, engine
from app.logger import logger

# ---------------------------------------------------------------------------
# Create all tables in the database on startup.
# In production you would use Alembic migrations instead (see alembic/ folder).
# ---------------------------------------------------------------------------
import app.models  # noqa: F401  ← ensures models are registered with Base

Base.metadata.create_all(bind=engine)
logger.info("Database tables created / verified ✓")


# ---------------------------------------------------------------------------
# Application instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "A clean, production-style FastAPI CRUD API for managing Users and Tasks.\n\n"
        "## Features\n"
        "- Full CRUD for **Users** and **Tasks**\n"
        "- Proper validation with Pydantic v2\n"
        "- Structured logging\n"
        "- Separation of concerns (models / schemas / services / controllers)\n"
    ),
    version="1.0.0",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc UI
)


# ---------------------------------------------------------------------------
# CORS middleware — allow all origins in dev, restrict in production
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Register routers
# ---------------------------------------------------------------------------
app.include_router(user_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")


# ---------------------------------------------------------------------------
# Health-check endpoint
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    """Quick liveness check used by load balancers / monitoring."""
    return {"status": "ok", "app": settings.APP_NAME}


# ---------------------------------------------------------------------------
# Startup / shutdown lifecycle hooks
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def on_startup():
    logger.info(f"🚀 {settings.APP_NAME} starting in '{settings.APP_ENV}' mode")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info(f"🛑 {settings.APP_NAME} shutting down")