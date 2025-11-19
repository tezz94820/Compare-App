"""
Logging Configuration
Centralized logging setup for the application
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

import config


def setup_logger(name: str = None) -> logging.Logger:
    """
    Set up and configure a logger instance
    
    Args:
        name: Logger name (usually __name__ of the module)
    
    Returns:
        Configured logger instance
    """
    # Use root logger if no name provided
    logger_name = name or "ComparisonTool"
    logger = logging.getLogger(logger_name)
    
    # Only configure if not already configured
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # File handler (rotating)
    log_file = config.LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=config.MAX_LOG_SIZE_MB * 1024 * 1024,
        backupCount=config.MAX_LOG_FILES,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance (shorthand for setup_logger)
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return setup_logger(name)


# ============================================================================
# GLOBAL APPLICATION LOGGER
# ============================================================================
app_logger = setup_logger("ComparisonTool")


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def log_info(message: str, logger_name: str = None):
    """Log an info message"""
    logger = get_logger(logger_name)
    logger.info(message)


def log_debug(message: str, logger_name: str = None):
    """Log a debug message"""
    logger = get_logger(logger_name)
    logger.debug(message)


def log_warning(message: str, logger_name: str = None):
    """Log a warning message"""
    logger = get_logger(logger_name)
    logger.warning(message)


def log_error(message: str, exc_info: bool = False, logger_name: str = None):
    """Log an error message"""
    logger = get_logger(logger_name)
    logger.error(message, exc_info=exc_info)


def log_critical(message: str, exc_info: bool = True, logger_name: str = None):
    """Log a critical error message"""
    logger = get_logger(logger_name)
    logger.critical(message, exc_info=exc_info)


def log_exception(exception: Exception, logger_name: str = None):
    """Log an exception with traceback"""
    logger = get_logger(logger_name)
    logger.exception(f"Exception occurred: {str(exception)}")