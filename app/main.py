import csv
import io
import logging
import os
import time
import uuid

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.cache import cache
from app.config import settings
from app.core import config_bridge
from app.core.logging_config import get_logger, setup_logging
from app.middleware.rate_limiter import RateLimitMiddleware
from app.middleware.request_logger import RequestLoggerMiddleware, log_request_middleware
from app.routes import api, health
from app.utils.env_debugger import log_environment_settings
from app.utils.error_handlers import (
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

# Determine log level from environment - priority to "LOG_LEVEL" over "DEBUG" flag for consistency
log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
try:
    log_level = getattr(logging, log_level_name)
except AttributeError:
    print(f"WARNING: Invalid LOG_LEVEL: {log_level_name}, using INFO")
    log_level = logging.INFO

# Setup logging with determined level
setup_logging(log_level)
logger = get_logger("main")

logger.info(f"Starting application with log level: {log_level_name}")

# Set Uvicorn's access logger to WARNING to avoid logging health checks
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize services, connections, etc.
    logger.info("Starting up JobSpy Docker API")
    
    # Log environment variables to help debugging
    log_environment_settings()
    
    # Yield control to the application
    yield
    
    # Shutdown: Clean up resources
    logger.info("Shutting down JobSpy Docker API")
    cache.clear()

# Create FastAPI app with enhanced documentation
app = FastAPI(
    title="JobSpy Docker API",
    description="""
    # JobSpy Docker API
    
    An API for searching jobs across multiple platforms including LinkedIn, Indeed, Glassdoor, Google, ZipRecruiter, Bayt, and Naukri.
    
    ## Authentication
    
    All API endpoints require an API key to be passed in the `x-api-key` header.
    
    ## Rate Limiting
    
    Requests are limited based on your API key. The default limit is 100 requests per hour.
    
    ## Caching
    
    Results are cached for 1 hour by default to improve performance and reduce load on job board sites.
    """,
    version="1.0.0",
    lifespan=lifespan,
    # Configure docs endpoints based on settings
    docs_url=settings.SWAGGER_UI_PATH if settings.ENABLE_SWAGGER_UI else None,
    redoc_url=settings.REDOC_PATH if settings.ENABLE_REDOC else None,
    openapi_tags=[
        {
            "name": "Jobs",
            "description": "Operations related to job searching",
        },
        {
            "name": "Health",
            "description": "API health check endpoints",
        },
        {
            "name": "Info",
            "description": "General API information",
        },
    ],
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Job Spy FastAPI application")
    # Additional startup logic can be added here

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Job Spy FastAPI application")
    # Additional shutdown logic can be added here

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Add request logging middleware
app.add_middleware(RequestLoggerMiddleware)

# Add exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Add request timing and logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Generate request ID for tracking
    request_id = str(uuid.uuid4())
    logger.debug(f"Request {request_id} started: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.debug(
            f"Request {request_id} completed: {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Time: {process_time:.3f}s"
        )
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        logger.exception(f"Request {request_id} failed: {str(e)}")
        raise

# Include routers
app.include_router(api.router, prefix="/api/v1", tags=["Jobs"])
app.include_router(health.router, tags=["Health"])

@app.get("/", tags=["Info"])
def read_root():
    return {
        "message": "Welcome to JobSpy Docker API!",
        "docs_url": "/docs",
        "api_root": "/api/v1",
        "health_check": "/health"
    }

# Add health check endpoint with minimal logging
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring systems"""
    # Only log health checks in debug mode
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Health check requested")
    return {"status": "healthy"}

@app.get("/api/v1/search_jobs")
async def search_jobs(
    # ...existing parameters...
    format: str = "json",
    # ...existing parameters...
):
    # ...existing code to get jobs as a list of dicts...
    jobs_data = ... # your existing jobs list/dict
    # ...existing code...

    if format == "csv":
        # Convert jobs_data to CSV
        if not jobs_data:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["No results"])
            output.seek(0)
            return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=jobs.csv"})
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=jobs_data[0].keys())
        writer.writeheader()
        writer.writerows(jobs_data)
        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=jobs.csv"})
    # Default: JSON
    return JSONResponse(content={"count": len(jobs_data), "jobs": jobs_data})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
