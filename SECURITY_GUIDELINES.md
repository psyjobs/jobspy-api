# Security Guidelines

## API Authentication
- Use `x-api-key` header; rotate keys regularly.
- Enforce HTTPS/TLS.

## Secrets Management
- Don’t commit `.env` with real keys.
- Use Docker secrets or Kubernetes Secrets.

## Dependencies
- Regularly run `pip install -U`.
- Audit with `safety` or `dependabot`.

## Vulnerability Reporting
- See `SECURITY.md` for reporting process.
