#!/usr/bin/env python3
"""
Script to explicitly load .env.local environment variables.
Run this script before starting the app if you want to use .env.local.
"""
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv is not installed. Please install it with:")
    print("pip install python-dotenv")
    sys.exit(1)

def load_local_env():
    """Explicitly load .env.local file if it exists."""
    env_local_path = Path(".env.local")
    
    if not env_local_path.exists():
        print(f"Warning: {env_local_path} not found")
        return False
    
    print(f"Loading environment variables from {env_local_path.absolute()}")
    load_dotenv(env_local_path, override=True)
    
    # Print a few non-sensitive variables to confirm loading
    print("Loaded variables (sample):")
    for var in ["LOG_LEVEL", "ENVIRONMENT", "ENABLE_CACHE"]:
        value = os.getenv(var, "[not set]")
        print(f"  {var}={value}")
    
    return True

if __name__ == "__main__":
    if load_local_env():
        print("\nSuccessfully loaded .env.local")
        print("Run your application now to use these variables")
    else:
        print("\nNo .env.local file found")
        print("Using default environment variables only")
