#!/bin/bash
# Script to set log level and restart the application

if [ -z "$1" ]; then
  echo "Usage: $0 <log_level>"
  echo "Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL"
  exit 1
fi

LOG_LEVEL=$(echo "$1" | tr '[:lower:]' '[:upper:]')
echo "Setting log level to: $LOG_LEVEL"

# Update .env file
sed -i.bak "s/^LOG_LEVEL=.*/LOG_LEVEL=$LOG_LEVEL/" .env

# Restart the service with new log level
echo "Restarting services..."
docker-compose down
LOG_LEVEL=$LOG_LEVEL docker-compose up -d

echo "Done! Services restarted with log level: $LOG_LEVEL"
echo "View logs with: docker-compose logs -f"
