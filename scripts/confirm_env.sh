#!/bin/bash
# Script to confirm environment variables are set correctly
# Run this at container startup

echo "=== Environment Variable Confirmation ==="
echo "ENABLE_API_KEY_AUTH: $ENABLE_API_KEY_AUTH"
echo "API_KEYS: ${API_KEYS:0:3}... (truncated for security)"
echo "RATE_LIMIT_ENABLED: $RATE_LIMIT_ENABLED"
echo "ENABLE_CACHE: $ENABLE_CACHE"
echo "LOG_LEVEL: $LOG_LEVEL"
echo "ENVIRONMENT: $ENVIRONMENT"
echo "========================================"
