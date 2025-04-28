"""Utility functions for checking authentication health."""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_auth_configuration() -> Dict[str, Any]:
    """
    Check the authentication configuration and return status details.
    This helps diagnose authentication issues by checking all relevant settings.
    """
    # Import here to avoid circular imports
    from app.core.config import settings as core_settings
    from app.config import settings as app_settings
    
    # Check core settings
    core_api_key_set = bool(core_settings.API_KEY)
    
    # Check app settings  
    app_auth_enabled = app_settings.ENABLE_API_KEY_AUTH
    app_keys_configured = bool(app_settings.API_KEYS)
    app_keys_count = len(app_settings.API_KEYS)
    
    # Check for configuration inconsistencies
    inconsistent_config = (app_keys_configured and not app_auth_enabled)
    
    # Generate recommendations
    recommendations = []
    if inconsistent_config:
        recommendations.append(
            "API keys are configured but authentication is disabled. Consider enabling ENABLE_API_KEY_AUTH."
        )
        logger.warning("API keys are configured but authentication is disabled. This may lead to unexpected behavior.")
    
    # Determine if authentication is needed based on both configs
    auth_required = core_api_key_set or (app_auth_enabled and app_keys_configured)
    
    # Log configuration sources
    logger.debug(f"API keys loaded from: {app_settings.API_KEYS_SOURCE}")
    logger.debug(f"Auth enabled setting loaded from: {app_settings.ENABLE_API_KEY_AUTH_SOURCE}")
    
    return {
        "auth_required": auth_required,
        "core_settings": {
            "api_key_configured": core_api_key_set,
        },
        "app_settings": {
            "auth_enabled": app_auth_enabled,
            "api_keys_configured": app_keys_configured,
            "api_keys_count": app_keys_count,
            "header_name": app_settings.API_KEY_HEADER_NAME,
            "api_keys_source": app_settings.API_KEYS_SOURCE,
            "auth_enabled_source": app_settings.ENABLE_API_KEY_AUTH_SOURCE,
        },
        "inconsistent_config": inconsistent_config,
        "recommendations": recommendations
    }
