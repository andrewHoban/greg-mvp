import sys
from typing import Any

from loguru import logger

from backend.app.config import get_settings


def configure_logging() -> None:
    """Configure Loguru logging with ISO timestamp format and environment-based level."""
    settings = get_settings()

    # Remove default handler
    logger.remove()

    # Add custom handler with ISO timestamp format
    log_format = (
        "<green>{time:YYYY-MM-DDTHH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.app_log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # Log configuration
    logger.info(f"Logging configured with level: {settings.app_log_level}")
    logger.info(f"Application environment: {settings.app_env}")


def get_logger_for_module(module_name: str) -> Any:
    """Get a logger instance for a specific module."""
    return logger.bind(name=module_name)
