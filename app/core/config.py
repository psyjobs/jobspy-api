from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Spy FastAPI"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: Optional[str] = None  # Made optional with default None
    API_KEY: Optional[str] = None

    # Logging settings
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_TO_FILE: bool = True
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @property
    def get_log_level(self):
        """Convert string log level to logging module level"""
        import logging
        return getattr(logging, self.LOG_LEVEL)

    class Config:
        case_sensitive = True

settings = Settings()