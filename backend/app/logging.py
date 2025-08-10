import sys

from loguru import logger


def setup_loguru():
    """Configure loguru logging with ISO format."""
    # Remove default handler
    logger.remove()
    
    # Add new handler with ISO timestamp format
    logger.add(
        sys.stdout,
        format=(
            "{time:YYYY-MM-DDTHH:mm:ss.SSS} | {level: <8} | "
            "{name}:{function}:{line} - {message}"
        ),
        level="INFO",
    )
    
    return logger