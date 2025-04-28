#!/bin/bash
# Script to debug the order of environment variable loading
# Run this to understand where each environment variable comes from

echo "=== Environment Variable Load Order Debug ==="

# Check different environment variable sources in order of precedence
echo "Environment variables from different sources:"
echo "1. Command line/docker-compose.yml environment section:"
echo "   LOG_LEVEL=$LOG_LEVEL"
echo "   ENABLE_API_KEY_AUTH=$ENABLE_API_KEY_AUTH"
echo 

# Check Dockerfile ENV vs runtime environment
echo "2. Default values from Dockerfile (these should be overridden at runtime):"
echo "   Dockerfile ARG LOG_LEVEL default=DEBUG"
echo "   Dockerfile ARG ENABLE_API_KEY_AUTH default=false"
echo 

# Dump all environment variables for analysis
echo "3. All current environment variables (alphabetical):"
env | grep -E "LOG_LEVEL|ENABLE_|API_KEY|ENVIRONMENT" | sort
echo

echo "=== Environment Variable Override Chain ==="
echo "Command line args > docker-compose environment > .env > Dockerfile ENV > Dockerfile ARG defaults"
echo "==========================================="
