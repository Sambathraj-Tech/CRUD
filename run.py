# run.py
# ---------------------------------------------------------------
# Entry point to start the development server.
# Run with:  python run.py
# ---------------------------------------------------------------

import uvicorn

from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.DEBUG,  # Auto-reload on file changes (dev only)
        log_level="debug" if settings.DEBUG else "info",
    )