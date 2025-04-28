# Architecture Overview

```
Client → API Gateway (FastAPI) → JobSpy Library → External Job APIs
                           ↓
                         Cache (Redis/File)
                           ↓
                         Logs/Monitoring
```

## Components
- FastAPI application (`app/main.py`)
- Caching layer (in‑memory or Redis)
- Rate limiter middleware
- Docker / Kubernetes deployment

## Data Flow
1. Client request with API key.
2. Check rate limit & cache.
3. Scrape job sites via JobSpy.
4. Return JSON/CSV response.
