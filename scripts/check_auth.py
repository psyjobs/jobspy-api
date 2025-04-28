#!/usr/bin/env python3
"""
Script to check API authentication configuration.
Run this script to debug issues with API key authentication.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_auth_config():
    """Print authentication configuration settings."""
    print("=== API Authentication Configuration ===")
    
    # Check environment variables
    env_vars = {
        "API_KEY": os.getenv("API_KEY", ""),
        "ENABLE_API_KEY_AUTH": os.getenv("ENABLE_API_KEY_AUTH", ""),
        "API_KEY_HEADER_NAME": os.getenv("API_KEY_HEADER_NAME", ""),
    }
    
    print("\nEnvironment Variables:")
    for key, value in env_vars.items():
        masked_value = "********" if key == "API_KEY" and value else value
        print(f"{key}={masked_value!r}")
    
    # Try to load app settings
    print("\nApp Settings:")
    try:
        from app.core.config import settings
        print(f"API_KEY configured: {bool(settings.API_KEY)}")
        print(f"API_KEY value is set: {bool(settings.API_KEY and settings.API_KEY != '')}")
    except Exception as e:
        print(f"Error loading settings: {e}")
    
    # Check .env file
    env_file = Path(".env")
    env_local_file = Path(".env.local")
    
    print("\nEnvironment Files:")
    print(f".env exists: {env_file.exists()}")
    print(f".env.local exists: {env_local_file.exists()}")
    
    # Provide troubleshooting tips
    print("\n=== Troubleshooting Tips ===")
    print("1. If you want to disable API key authentication:")
    print("   - Ensure API_KEY is not set in your environment or .env files")
    print("   - Or explicitly set API_KEY='' (empty string) in your .env file")
    print("\n2. If you want to enable API key authentication:")
    print("   - Set API_KEY='your-secret-key' in your .env.local file")
    print("   - Include the X-API-Key header in your requests")
    print("\n3. To see detailed authentication logs:")
    print("   - Set LOG_LEVEL=DEBUG in your environment or .env file")

if __name__ == "__main__":
    check_auth_config()
