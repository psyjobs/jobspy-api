import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(log_level=None):
    """Configure logging for the application"""
    
    # Determine log level from environment or parameter
    if log_level is None:
        env_level = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, env_level, logging.INFO)
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Clear existing handlers to avoid duplicate logs
    if logger.handlers:
        logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # File handler with rotation (10MB max, keep 5 backups)
    file_handler = RotatingFileHandler(
        "logs/app.log", 
        maxBytes=10*1024*1024, 
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Set Uvicorn's access logger to a higher level to reduce noise
    uvicorn_access = logging.getLogger("uvicorn.access")
    if log_level == logging.DEBUG:
        uvicorn_access.setLevel(logging.INFO)  # Show access logs in debug mode, but not health checks
    else:
        uvicorn_access.setLevel(logging.WARNING)  # Only show warnings and errors otherwise
        
    # Return the configured logger
    return logger

def get_logger(name):
    """Get a named logger"""
    return logging.getLogger(name)
