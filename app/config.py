# app/config.py
# ---------------------------------------------------------------
# Centralized configuration loaded from environment variables.
# Pydantic's BaseSettings automatically reads from .env files.
# ---------------------------------------------------------------

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All values can be overridden via a .env file at the project root.
    """

    # --- Database ---
    DATABASE_URL: str = "postgresql://postgres:12345@localhost:5432/crud_db"

    # --- App metadata ---
    APP_NAME: str = "FastAPI CRUD App"
    APP_ENV: str = "development"
    APP_PORT: int = 8000
    DEBUG: bool = True

    # --- Security ---
    SECRET_KEY: str = "change-me-in-production"

    # Tell Pydantic to read from the .env file automatically
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Create a single shared instance — import this everywhere
settings = Settings()