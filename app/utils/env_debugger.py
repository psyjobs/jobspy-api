"""Utility to debug environment variable loading."""
import logging
import os

logger = logging.getLogger(__name__)

def log_environment_settings():
    """
    Log all environment variables relevant to application configuration.
    This helps diagnose when environment variables aren't being loaded correctly.
    """
    env_vars = {
        "API_KEYS": os.getenv("API_KEYS", "[not set]"),
        "ENABLE_API_KEY_AUTH": os.getenv("ENABLE_API_KEY_AUTH", "[not set]"),
        "API_KEY_HEADER_NAME": os.getenv("API_KEY_HEADER_NAME", "[not set]"),
        "RATE_LIMIT_ENABLED": os.getenv("RATE_LIMIT_ENABLED", "[not set]"),
        "RATE_LIMIT_REQUESTS": os.getenv("RATE_LIMIT_REQUESTS", "[not set]"),
        "RATE_LIMIT_TIMEFRAME": os.getenv("RATE_LIMIT_TIMEFRAME", "[not set]"),
        "DEFAULT_PROXIES": os.getenv("DEFAULT_PROXIES", "[not set]"),
        "DEFAULT_SITE_NAMES": os.getenv("DEFAULT_SITE_NAMES", "[not set]"),
        "ENABLE_CACHE": os.getenv("ENABLE_CACHE", "[not set]"),
        "CACHE_EXPIRY": os.getenv("CACHE_EXPIRY", "[not set]"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "[not set]"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "[not set]"),
    }

    # Mask sensitive values
    if env_vars["API_KEYS"] != "[not set]":
        env_vars["API_KEYS"] = "****[MASKED]****"

    # Log all relevant environment variables
    logger.info("Environment variables loaded:")
    for key, value in env_vars.items():
        logger.info(f"  {key}={value}")

    return env_vars
