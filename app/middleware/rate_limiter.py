import time
from collections import defaultdict
from typing import DefaultDict, Dict, List

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from app.config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limits: DefaultDict[str, List[float]] = defaultdict(list)
        self.enabled = settings.RATE_LIMIT_ENABLED
        self.max_requests = settings.RATE_LIMIT_REQUESTS
        self.timeframe = settings.RATE_LIMIT_TIMEFRAME
        self._last_cleanup = time.time()
        self._cleanup_interval = 300  # Clean up every 5 minutes
    
    def _cleanup_old_entries(self, current_time: float):
        """Remove old entries and empty client identifiers to prevent memory leaks."""
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        # Remove entries older than timeframe and empty identifiers
        to_remove = []
        for client_id, timestamps in self.rate_limits.items():
            # Filter out old timestamps
            self.rate_limits[client_id] = [
                ts for ts in timestamps 
                if current_time - ts < self.timeframe
            ]
            # Mark empty entries for removal
            if not self.rate_limits[client_id]:
                to_remove.append(client_id)
        
        # Remove empty entries
        for client_id in to_remove:
            del self.rate_limits[client_id]
        
        self._last_cleanup = current_time
    
    async def dispatch(self, request: Request, call_next):
        if not self.enabled:
            return await call_next(request)
        
        # Get client identifier (use API key if available, otherwise IP)
        client_identifier = request.headers.get(settings.API_KEY_HEADER_NAME, request.client.host)
        
        # Check rate limit
        current_time = time.time()
        
        # Periodic cleanup to prevent memory leaks
        self._cleanup_old_entries(current_time)
        
        # Clean up old request timestamps for this client
        self.rate_limits[client_identifier] = [
            timestamp for timestamp in self.rate_limits[client_identifier] 
            if current_time - timestamp < self.timeframe
        ]
        
        # Check if rate limit exceeded
        if len(self.rate_limits[client_identifier]) >= self.max_requests:
            reset_time = min(self.rate_limits[client_identifier]) + self.timeframe - current_time
            headers = {"X-RateLimit-Reset": str(int(reset_time))}
            
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.max_requests} requests per {self.timeframe} seconds.",
                headers=headers
            )
        
        # Add current request timestamp
        self.rate_limits[client_identifier].append(current_time)
        
        # Process the request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self.max_requests - len(self.rate_limits[client_identifier])
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
