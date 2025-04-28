#!/usr/bin/env python3
"""
Script to verify that environment variables are being properly loaded.
Run this script to compare .env values with actual loaded values.
"""
import os
import sys
from pathlib import Path
import dotenv

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def verify_env_loading():
    """Verify environment variables are loaded correctly from .env files."""
    print("=== Environment Variable Loading Verification ===\n")
    
    # Load .env file content to compare with actual environment variables
    env_file = Path(".env")
    env_local_file = Path(".env.local")
    
    env_vars = {}
    if env_file.exists():
        print(f"Loading .env file from {env_file.absolute()}")
        env_vars.update(dotenv.dotenv_values(env_file))
    else:
        print(".env file not found")
    
    # Check if .env.local exists, but note that it's not loaded by default
    if env_local_file.exists():
        print(f"Found .env.local file at {env_local_file.absolute()}")
        print("NOTE: .env.local is not automatically loaded by the application.")
        print("To use .env.local, you must explicitly load it or use docker-compose.dev.yml")
        
        # Still load it for debugging purposes
        local_vars = dotenv.dotenv_values(env_local_file)
        print(f"  .env.local contains {len(local_vars)} variables")
    else:
        print(".env.local file not found")
    
    print("\n=== Expected vs Actual Values ===")
    for key, expected_value in env_vars.items():
        actual_value = os.getenv(key)
        match = expected_value == actual_value
        status = "✅" if match else "❌"
        
        # Mask API keys
        if "API_KEY" in key and expected_value:
            expected_value = "****[MASKED]****"
        if "API_KEY" in key and actual_value:
            actual_value = "****[MASKED]****"
            
        print(f"{status} {key}:")
        print(f"  Expected: {expected_value!r}")
        print(f"  Actual:   {actual_value!r}")
    
    print("\n=== Docker Environment Note ===")
    print("If running in Docker, environment values in docker-compose.yml")
    print("will override values from .env files. To fix this:")
    print("1. Use ${VAR_NAME:-default} syntax in docker-compose.yml")
    print("2. Use the env_file directive to load .env files")
    print("3. Ensure .env files are mounted/copied to the container")

if __name__ == "__main__":
    try:
        import dotenv
    except ImportError:
        print("python-dotenv package is required to run this script.")
        print("Install it with: pip install python-dotenv")
        sys.exit(1)
        
    verify_env_loading()
