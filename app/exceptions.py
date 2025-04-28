"""Custom exception classes for JobSpy Docker API."""
from fastapi import HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

class JobSpyAPIException(HTTPException):
    """Base exception for JobSpy Docker API."""
    def __init__(self, status_code: int, detail: str, headers: dict = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class RateLimitExceeded(JobSpyAPIException):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(status_code=HTTP_429_TOO_MANY_REQUESTS, detail=detail)

class InvalidSearchParameters(JobSpyAPIException):
    """Exception raised when search parameters are invalid."""
    def __init__(self, detail: str = "Invalid search parameters"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class JobSearchError(JobSpyAPIException):
    """Exception raised when job search fails."""
    def __init__(self, detail: str = "Job search failed"):
        super().__init__(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
