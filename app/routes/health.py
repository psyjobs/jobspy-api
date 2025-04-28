from fastapi import APIRouter, Request, Depends, HTTPException, status
from app.models import HealthCheck
from app.core.config import settings as core_settings
from app.config import settings as app_settings
import logging
import os
import platform
import time
from app.utils.auth_health import check_auth_configuration

router = APIRouter()
logger = logging.getLogger(__name__)

# Create a dependency to check if health endpoints are enabled
async def verify_health_enabled():
    """Verify that health endpoints are enabled via configuration."""
    if not app_settings.ENABLE_HEALTH_ENDPOINTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health endpoints are disabled"
        )
    return True

@router.get("/health", response_model=HealthCheck, tags=["Health"], dependencies=[Depends(verify_health_enabled)])
async def health_check():
    """
    Health check endpoint to verify the API is running correctly and return system status
    """
    # Get authentication status
    auth_status = check_auth_configuration()
    
    # Build response with all the requested information
    return HealthCheck(
        status="ok",
        version="1.0.0",
        environment=app_settings.ENVIRONMENT,
        log_level=app_settings.LOG_LEVEL,
        auth={
            "enabled": app_settings.ENABLE_API_KEY_AUTH,
            "api_keys_configured": bool(app_settings.API_KEYS),
            "api_keys_count": len(app_settings.API_KEYS) if app_settings.API_KEYS else 0,
            "inconsistent": auth_status["inconsistent_config"],
        },
        rate_limiting={
            "enabled": app_settings.RATE_LIMIT_ENABLED,
            "requests_limit": app_settings.RATE_LIMIT_REQUESTS,
            "timeframe_seconds": app_settings.RATE_LIMIT_TIMEFRAME,
        },
        cache={
            "enabled": app_settings.ENABLE_CACHE,
            "expiry_seconds": app_settings.CACHE_EXPIRY,
        },
        health_endpoints={
            "enabled": app_settings.ENABLE_HEALTH_ENDPOINTS,
            "detailed_health": app_settings.ENABLE_DETAILED_HEALTH,
        },
        config={
            "default_site_names": app_settings.DEFAULT_SITE_NAMES,
            "default_results_wanted": app_settings.DEFAULT_RESULTS_WANTED,
            "default_distance": app_settings.DEFAULT_DISTANCE,
            "default_description_format": app_settings.DEFAULT_DESCRIPTION_FORMAT,
            "default_country_indeed": app_settings.DEFAULT_COUNTRY_INDEED,
        },
        timestamp=time.time()
    )

@router.get("/ping", tags=["Health"], dependencies=[Depends(verify_health_enabled)])
async def ping():
    """
    Simple ping endpoint for load balancers and monitoring
    """
    return {"status": "ok"}

@router.get("/auth-status", tags=["Health"], dependencies=[Depends(verify_health_enabled)])
async def auth_status(request: Request):
    """
    Diagnostic endpoint to check authentication settings
    """
    logger.info("Auth status endpoint called")
    
    # Check if the request has the API key header
    api_key_header_name = "X-API-Key"
    api_key_in_request = request.headers.get(api_key_header_name)
    
    return {
        "api_key_configured": bool(core_settings.API_KEY),
        "api_key_header_name": api_key_header_name,
        "api_key_in_request": bool(api_key_in_request),
        "authentication_enabled": bool(core_settings.API_KEY),
        "environment": core_settings.ENVIRONMENT if hasattr(core_settings, "ENVIRONMENT") else app_settings.ENVIRONMENT
    }

@router.get("/api-config", tags=["Health"], dependencies=[Depends(verify_health_enabled)])
async def api_config():
    """
    Diagnostic endpoint to check API configuration settings
    """
    logger.info("API configuration endpoint called")
    
    # Only provide detailed info if it's enabled
    if not app_settings.ENABLE_DETAILED_HEALTH:
        return {
            "status": "ok",
            "message": "Detailed health information is disabled. Enable with ENABLE_DETAILED_HEALTH=true"
        }
    
    # Build comprehensive config information
    system_info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
    }
    
    # Configuration information
    config = {
        "environment": app_settings.ENVIRONMENT,
        "log_level": app_settings.LOG_LEVEL,
        "authentication": {
            "enabled": app_settings.ENABLE_API_KEY_AUTH,
            "api_keys_configured": bool(app_settings.API_KEYS),
            "api_keys_count": len(app_settings.API_KEYS) if app_settings.API_KEYS else 0,
            "header_name": app_settings.API_KEY_HEADER_NAME,
        },
        "rate_limiting": {
            "enabled": app_settings.RATE_LIMIT_ENABLED,
            "requests_limit": app_settings.RATE_LIMIT_REQUESTS,
            "timeframe_seconds": app_settings.RATE_LIMIT_TIMEFRAME,
        },
        "caching": {
            "enabled": app_settings.ENABLE_CACHE,
            "expiry_seconds": app_settings.CACHE_EXPIRY,
        },
        "health_endpoints": {
            "enabled": app_settings.ENABLE_HEALTH_ENDPOINTS,
            "detailed_health": app_settings.ENABLE_DETAILED_HEALTH,
        },
    }
    
    return {
        "status": "ok",
        "system": system_info,
        "config": config,
        "timestamp": time.time()
    }

@router.get("/config-sources", tags=["Health"], dependencies=[Depends(verify_health_enabled)])
async def config_sources():
    """
    Diagnostic endpoint to view the source of each configuration setting
    """
    logger.info("Configuration sources endpoint called")
    
    # Only provide detailed info if it's enabled
    if not app_settings.ENABLE_DETAILED_HEALTH:
        return {
            "status": "ok",
            "message": "Detailed health information is disabled. Enable with ENABLE_DETAILED_HEALTH=true"
        }
    
    # Get all settings with their sources
    settings_with_sources = app_settings.get_all_settings()
    
    # Format for output, focusing on key settings
    important_settings = [
        "ENABLE_API_KEY_AUTH", "API_KEYS", "RATE_LIMIT_ENABLED", 
        "ENABLE_CACHE", "ENVIRONMENT", "LOG_LEVEL"
    ]
    
    focused_settings = {k: settings_with_sources[k] for k in important_settings if k in settings_with_sources}
    
    # Check for configuration inconsistencies
    auth_status = check_auth_configuration()
    inconsistencies = []
    
    if auth_status["inconsistent_config"]:
        inconsistencies.extend(auth_status["recommendations"])
    
    return {
        "status": "ok",
        "key_settings": focused_settings,
        "all_settings": settings_with_sources,
        "inconsistencies": inconsistencies,
        "timestamp": time.time()
    }
