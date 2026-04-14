# app/logger.py
# ---------------------------------------------------------------
# Centralized logging configuration.
# Import `logger` from here in every module that needs logging.
# ---------------------------------------------------------------

import logging
import sys

from app.config import settings


def setup_logger(name: str = "fastapi-crud") -> logging.Logger:
    """
    Create and return a configured logger instance.

    - INFO level in production
    - DEBUG level in development (controlled by DEBUG env var)
    - Logs go to stdout so they appear in Docker / systemd / cloud logs
    """
    logger = logging.getLogger(name)

    # Set log level based on DEBUG env variable
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logger.setLevel(log_level)

    # Avoid adding duplicate handlers if called multiple times
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)

        # Human-readable format: timestamp | level | module | message
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Single shared logger for the whole app
logger = setup_logger()