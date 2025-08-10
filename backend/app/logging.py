"""
Logging configuration using Loguru
"""

import sys
from typing import Any, Dict

from loguru import logger

from .config import settings


def configure_logging() -> None:
    """Configure Loguru logger for the application."""
    
    # Remove default handler
    logger.remove()
    
    # Configure format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    
    # Add console handler
    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    # TODO: Add file handler for production
    # logger.add(
    #     "logs/app.log",
    #     format=log_format,
    #     level="INFO",
    #     rotation="10 MB",
    #     retention="10 days",
    #     compression="zip",
    # )


def get_logger(name: str) -> Any:
    """Get a logger instance with the given name."""
    configure_logging()
    return logger.bind(name=name)