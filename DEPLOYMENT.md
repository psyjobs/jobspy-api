# Deployment Guide

## Production (Docker Compose)
1. Copy `.env.example` → `.env` and fill in values.
2. `docker-compose up -d`
3. Verify: `docker-compose logs jobspy-api`

## Standalone Docker
```bash
docker build -t jobspy-api:latest .
docker run -d -p 8000:8000 \
  --env-file .env \
  jobspy-api:latest
```

## Kubernetes (example)
- Define Deployment, Service, ConfigMap for env vars.
- Mount `ca_cert` as a Secret if needed.
