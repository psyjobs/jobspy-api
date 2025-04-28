"""Documentation for logging levels and troubleshooting."""

LOGGING_LEVELS = {
    "DEBUG": {
        "level": 10,
        "description": "Detailed information, typically of interest only when diagnosing problems",
        "use_case": "Shows detailed flow of the application, including variable values and decision points",
        "shows_auth_errors": True,
        "environment": "Development"
    },
    "INFO": {
        "level": 20,
        "description": "Confirmation that things are working as expected",
        "use_case": "Normal operation events like startup, shutdown, or successful requests",
        "shows_auth_errors": False,
        "environment": "Development/Production"
    },
    "WARNING": {
        "level": 30,
        "description": "Indication that something unexpected happened, or may happen in the near future",
        "use_case": "Non-critical issues like deprecation notices or improper usage",
        "shows_auth_errors": True,
        "environment": "Development/Production"
    },
    "ERROR": {
        "level": 40,
        "description": "Due to a more serious problem, the software has not been able to perform some function",
        "use_case": "Exception handling and error conditions that should be investigated",
        "shows_auth_errors": True,
        "environment": "Development/Production"
    },
    "CRITICAL": {
        "level": 50,
        "description": "A very serious error, indicating that the program itself may be unable to continue running",
        "use_case": "Application crashes and severe system issues",
        "shows_auth_errors": True,
        "environment": "Development/Production"
    }
}

def get_appropriate_level_for_issue(issue_type):
    """Get the appropriate logging level for different issue types."""
    issue_levels = {
        "auth": ["DEBUG", "WARNING"],
        "api_key": ["DEBUG", "WARNING"],
        "request_validation": ["DEBUG", "WARNING"],
        "server_error": ["ERROR", "CRITICAL"],
        "rate_limit": ["WARNING"],
        "performance": ["DEBUG", "INFO"]
    }
    return issue_levels.get(issue_type, ["DEBUG"])

def get_troubleshooting_tips():
    """Get troubleshooting tips for common issues."""
    return {
        "authentication_issues": [
            "Check if API_KEY is set in your environment or .env file",
            "Verify your requests include the X-API-Key header with the correct value",
            "Try the /auth-status endpoint to check current authentication settings",
            "Set LOG_LEVEL=DEBUG to see detailed authentication logging"
        ],
        "missing_api_key_error": [
            "This error occurs when API_KEY is configured but not included in your request",
            "Either add the X-API-Key header to your request or remove the API_KEY from your settings"
        ],
        "invalid_api_key_error": [
            "This error occurs when the API key in your request doesn't match the configured value",
            "Check the API_KEY value in your environment or .env file"
        ],
        "server_errors": [
            "Check the application logs for details about the error",
            "Ensure all required environment variables are set",
            "Verify the application has appropriate permissions"
        ]
    }
