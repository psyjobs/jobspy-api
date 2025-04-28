# Upgrade Guide

## From v1.x to v2.0
1. Review breaking changes in `API_CHANGELOG.md`.
2. Update Docker image tag to `username/jobspy-api:2.0.0`.
3. Migrate environment vars: new OAuth2 settings.
4. Run integration tests against staging.

## Patch Releases
```bash
make docker-pull && make docker-compose-down && make docker-compose-up -d
```
