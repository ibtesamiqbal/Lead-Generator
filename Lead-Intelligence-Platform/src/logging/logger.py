"""
Structured Logging Module for Lead Intelligence Platform.
Uses rich for styled terminal output with fallback to standard logging.
"""

import logging
import sys
from rich.logging import RichHandler
from src.config.settings import settings


def setup_logger(name: str = "lead_intel") -> logging.Logger:
    """Configures and returns a logger instance with rich formatting."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    log_level = logging.DEBUG if settings.debug else logging.INFO
    logger.setLevel(log_level)

    try:
        handler = RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_path=False,
            markup=True
        )
    except Exception:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

    handler.setLevel(log_level)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


logger = setup_logger()
