"""Logging configuration for JobSpy Docker API."""
import logging
import logging.config
import os
from pathlib import Path

def setup_logging(log_level: str = "INFO"):
    """Configure logging for the application."""
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": log_level,
            },
        },
        "loggers": {
            "": {"level": log_level, "handlers": ["console"], "propagate": True},
            "app": {"level": log_level, "handlers": ["console"], "propagate": False},
            "uvicorn": {"level": log_level, "handlers": ["console"], "propagate": False},
        },
    }
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Add file handler if not in development mode
    if os.environ.get("ENVIRONMENT", "development") != "development":
        log_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "level": log_level,
        }
        log_config["loggers"][""]["handlers"].append("file")
        log_config["loggers"]["app"]["handlers"].append("file")
    
    logging.config.dictConfig(log_config)
