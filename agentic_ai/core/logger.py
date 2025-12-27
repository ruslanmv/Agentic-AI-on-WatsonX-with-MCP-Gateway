"""
Logging configuration and utilities.

This module provides a centralized logging configuration using loguru
for structured, colorful, and easily filterable logs across the application.
"""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger


class LoggerConfig:
    """
    Configuration class for application logging.

    This class manages the logging setup, providing structured logging
    with file rotation, colored output, and configurable log levels.
    """

    _configured: bool = False

    @classmethod
    def configure(
        cls,
        log_level: str = "INFO",
        log_file: Optional[Path] = None,
        rotation: str = "10 MB",
        retention: str = "1 week",
        format_string: Optional[str] = None,
    ) -> None:
        """
        Configure the application logger.

        Args:
            log_level: Minimum log level to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for log output. If None, logs only to console
            rotation: When to rotate log files (e.g., "10 MB", "1 day")
            retention: How long to keep old log files
            format_string: Custom format string. If None, uses default format

        Example:
            >>> LoggerConfig.configure(log_level="DEBUG", log_file=Path("app.log"))
        """
        if cls._configured:
            return

        # Remove default handler
        logger.remove()

        # Default format with colors and structure
        if format_string is None:
            format_string = (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )

        # Console handler with colors
        logger.add(
            sys.stderr,
            format=format_string,
            level=log_level,
            colorize=True,
            backtrace=True,
            diagnose=True,
        )

        # File handler if specified
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            logger.add(
                str(log_file),
                format=format_string,
                level=log_level,
                rotation=rotation,
                retention=retention,
                compression="zip",
                backtrace=True,
                diagnose=True,
            )

        cls._configured = True
        logger.info(f"Logger configured with level: {log_level}")


def get_logger(name: Optional[str] = None) -> "logger":  # type: ignore[name-defined]
    """
    Get a logger instance.

    This function returns a configured logger instance. If the logger
    hasn't been configured yet, it will be configured with default settings.

    Args:
        name: Optional logger name for context. If None, uses the calling module name

    Returns:
        Configured logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    if not LoggerConfig._configured:
        LoggerConfig.configure()

    if name:
        return logger.bind(name=name)
    return logger


# Convenience function for structured logging
def log_exception(
    exception: Exception,
    context: Optional[dict[str, str]] = None,
    level: str = "ERROR",
) -> None:
    """
    Log an exception with structured context.

    Args:
        exception: The exception to log
        context: Optional dictionary with additional context
        level: Log level to use (ERROR, WARNING, CRITICAL)

    Example:
        >>> try:
        ...     risky_operation()
        ... except Exception as e:
        ...     log_exception(e, context={"user_id": "123", "action": "login"})
    """
    log_func = getattr(logger, level.lower())
    context_str = f" | Context: {context}" if context else ""
    log_func(f"Exception occurred: {type(exception).__name__}: {exception}{context_str}")
    logger.exception(exception)
