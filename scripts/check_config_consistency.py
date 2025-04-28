#!/usr/bin/env python3
"""
Script to check for configuration consistency across different settings files.
This helps identify and resolve inconsistencies in environment variables.
"""
import os
import sys
import yaml
import dotenv
from pathlib import Path
import re
from typing import Dict, Any, List, Set

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def color_text(text, color_code):
    """Add color to terminal output."""
    return f"\033[{color_code}m{text}\033[0m"

def red(text):
    return color_text(text, 31)

def green(text):
    return color_text(text, 32)

def yellow(text):
    return color_text(text, 33)

def blue(text):
    return color_text(text, 34)

def load_env_file(path: Path) -> Dict[str, str]:
    """Load environment variables from a .env file."""
    if not path.exists():
        print(f"Warning: {path} not found")
        return {}
    
    return dotenv.dotenv_values(path)

def extract_dockerfile_env_vars(path: Path) -> Dict[str, str]:
    """Extract environment variables from a Dockerfile."""
    if not path.exists():
        print(f"Warning: {path} not found")
        return {}
    
    env_vars = {}
    try:
        with open(path, 'r') as f:
            content = f.read()
            
        # Look for ENV statements
        # This is a simple approach - a proper parser would be better
        env_pattern = r'ENV\s+([A-Za-z0-9_]+)=([^\s\\]+)'
        simple_envs = re.findall(env_pattern, content)
        for key, value in simple_envs:
            env_vars[key] = value.strip('"\'')
            
        # Look for multi-line ENV statements
        multi_pattern = r'ENV\s+([A-Za-z0-9_]+)=([^\s\\]+)(\s*\\\s*\n\s*([A-Za-z0-9_]+)=([^\s\\]+))*'
        multi_envs = re.findall(multi_pattern, content)
        for match in multi_envs:
            for i in range(0, len(match), 3):
                if i+1 < len(match) and match[i] and match[i+1]:
                    env_vars[match[i]] = match[i+1].strip('"\'')
    except Exception as e:
        print(f"Error parsing Dockerfile: {e}")
    
    return env_vars

def load_docker_compose_vars(path: Path) -> Dict[str, str]:
    """Load environment variables from a docker-compose file."""
    if not path.exists():
        print(f"Warning: {path} not found")
        return {}
    
    try:
        with open(path, 'r') as f:
            compose_data = yaml.safe_load(f)
        
        env_vars = {}
        for service_name, service_data in compose_data.get('services', {}).items():
            # Check environment section
            environment = service_data.get('environment', [])
            if isinstance(environment, list):
                for env in environment:
                    if isinstance(env, str) and '=' in env:
                        key, value = env.split('=', 1)
                        # Handle ${VAR:-default} format
                        if '${' in value and ':-' in value and '}' in value:
                            default_val = value.split(':-')[1].split('}')[0]
                            env_vars[key] = default_val
                        else:
                            env_vars[key] = value
            elif isinstance(environment, dict):
                env_vars.update(environment)
        
        return env_vars
    except Exception as e:
        print(f"Error parsing docker-compose file: {e}")
        return {}

def check_config_consistency():
    """Check configuration consistency across different settings files."""
    print(yellow("=== Configuration Consistency Checker ===\n"))
    
    # Define paths to all configuration files
    env_path = Path(".env")
    env_local_path = Path(".env.local")
    dockerfile_path = Path("Dockerfile")
    docker_compose_path = Path("docker-compose.yml")
    docker_compose_dev_path = Path("docker-compose.dev.yml")
    
    # Load environment variables from each file
    env_vars = load_env_file(env_path)
    env_local_vars = load_env_file(env_local_path)
    dockerfile_vars = extract_dockerfile_env_vars(dockerfile_path)
    docker_compose_vars = load_docker_compose_vars(docker_compose_path)
    docker_compose_dev_vars = load_docker_compose_vars(docker_compose_dev_path)
    
    # Collect all variable names across all files
    all_vars = set()
    all_vars.update(env_vars.keys())
    all_vars.update(env_local_vars.keys())
    all_vars.update(dockerfile_vars.keys())
    all_vars.update(docker_compose_vars.keys())
    all_vars.update(docker_compose_dev_vars.keys())
    
    # Filter out non-app related environment variables
    excluded_vars = {'PYTHONDONTWRITEBYTECODE', 'PYTHONUNBUFFERED', 'PYTHONPATH'}
    app_vars = all_vars - excluded_vars
    
    # Check for presence of each variable in each file
    print(yellow("Checking variable presence in each configuration file:"))
    missing_vars = {
        ".env": [],
        ".env.local": [],
        "Dockerfile": [],
        "docker-compose.yml": [],
        "docker-compose.dev.yml": []
    }
    
    for var in sorted(app_vars):
        print(f"\n{blue(var)}:")
        
        if var not in env_vars:
            missing_vars[".env"].append(var)
            print(f"  .env: {red('MISSING')}")
        else:
            print(f"  .env: {env_vars[var]}")
            
        if var not in env_local_vars:
            # Only mark as missing if uncommented in .env.local
            print(f"  .env.local: {yellow('Not specified')}")
        else:
            print(f"  .env.local: {env_local_vars[var]}")
            
        if var not in dockerfile_vars:
            missing_vars["Dockerfile"].append(var)
            print(f"  Dockerfile: {red('MISSING')}")
        else:
            print(f"  Dockerfile: {dockerfile_vars[var]}")
            
        if var not in docker_compose_vars:
            missing_vars["docker-compose.yml"].append(var)
            print(f"  docker-compose.yml: {red('MISSING')}")
        else:
            print(f"  docker-compose.yml: {docker_compose_vars[var]}")
            
        if var not in docker_compose_dev_vars:
            missing_vars["docker-compose.dev.yml"].append(var)
            print(f"  docker-compose.dev.yml: {red('MISSING')}")
        else:
            print(f"  docker-compose.dev.yml: {docker_compose_dev_vars[var]}")
    
    # Print summary of missing variables
    print("\n" + yellow("=== Missing Variables Summary ==="))
    for file_path, vars_list in missing_vars.items():
        if vars_list:
            print(f"\n{file_path} is missing these variables:")
            for var in vars_list:
                print(f"  - {var}")
    
    # Check for inconsistent default values
    print("\n" + yellow("=== Inconsistent Default Values ==="))
    inconsistent_defaults = []
    for var in sorted(app_vars):
        values = {}
        if var in env_vars:
            values[".env"] = env_vars[var]
        if var in dockerfile_vars:
            values["Dockerfile"] = dockerfile_vars[var]
        
        # Skip if we don't have at least two sources to compare
        if len(values) < 2:
            continue
            
        # Check if values are inconsistent
        if len(set(values.values())) > 1:
            inconsistent_defaults.append((var, values))
    
    if inconsistent_defaults:
        for var, values in inconsistent_defaults:
            print(f"\n{red(var)} has inconsistent default values:")
            for source, value in values.items():
                print(f"  {source}: {value}")
    else:
        print(green("No inconsistencies found in default values!"))
    
    # Provide recommendations
    print("\n" + yellow("=== Recommendations ==="))
    
    if missing_vars[".env"]:
        print("\n1. Add these missing variables to .env:")
        for var in missing_vars[".env"]:
            # Try to find a default value from other files
            default_val = docker_compose_vars.get(var) or dockerfile_vars.get(var) or ""
            print(f"   {var}={default_val}")
    
    if missing_vars["Dockerfile"]:
        print("\n2. Consider adding these variables to Dockerfile ENV section:")
        for var in missing_vars["Dockerfile"]:
            # Try to find a default value from other files
            default_val = env_vars.get(var) or docker_compose_vars.get(var) or ""
            print(f"   {var}={default_val}")
    
    print("\n3. Ensure docker-compose.dev.yml loads from .env:")
    print("   Add this to the service configuration:")
    print("   env_file:")
    print("     - .env")
    
    if inconsistent_defaults:
        print("\n4. Fix inconsistent default values between files")

if __name__ == "__main__":
    try:
        check_config_consistency()
    except Exception as e:
        print(red(f"Error: {e}"))
        import traceback
        traceback.print_exc()
