#!/usr/bin/env python3
"""
Script to increment the version number in the app's __init__.py file.
Usage: python increment_version.py [major|minor|patch]
"""
import re
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
init_file = project_root / "app" / "__init__.py"

def read_version():
    """Read the current version from __init__.py"""
    content = init_file.read_text()
    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not version_match:
        raise ValueError("Could not find version string in __init__.py")
    return version_match.group(1)

def write_version(new_version):
    """Write the new version to __init__.py"""
    content = init_file.read_text()
    new_content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{new_version}"',
        content
    )
    init_file.write_text(new_content)

def increment_version(version_part):
    """
    Increment the version number.
    version_part: 'major', 'minor', or 'patch'
    """
    current = read_version()
    print(f"Current version: {current}")
    
    try:
        major, minor, patch = map(int, current.split('.'))
    except ValueError:
        print(f"Error: Version {current} is not in the format X.Y.Z")
        sys.exit(1)
    
    if version_part == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_part == "minor":
        minor += 1
        patch = 0
    elif version_part == "patch":
        patch += 1
    else:
        print(f"Error: Unknown version part '{version_part}'. Use 'major', 'minor', or 'patch'")
        sys.exit(1)
    
    new_version = f"{major}.{minor}.{patch}"
    write_version(new_version)
    print(f"Version updated to: {new_version}")
    return new_version

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["major", "minor", "patch"]:
        print("Usage: python increment_version.py [major|minor|patch]")
        sys.exit(1)
    
    increment_version(sys.argv[1])
