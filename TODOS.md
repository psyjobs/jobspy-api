# TODOS

## P2: Migrate to Redis cache
- **What:** Replace in-memory dict cache with Redis
- **Why:** In-memory cache is lost on worker recycling (each worker has its own cache). Redis enables cache sharing between workers and future multi-instance scaling.
- **Effort:** M (human) → S with CC
- **Depends on:** Redis infrastructure (docker-compose service or external Redis)
- **Added:** 2026-03-27 (CEO review of stability fix)

## P3: Remove duplicate search_jobs endpoint from app/main.py
- **What:** Delete the dead `/api/v1/search_jobs` endpoint at app/main.py:196-276
- **Why:** Dead code with `jobs_data = []` placeholder. Confusing and could mask routing issues.
- **Effort:** S → S with CC
- **Depends on:** Nothing
- **Added:** 2026-03-27 (CEO review of stability fix)

## P3: Replace BaseHTTPMiddleware with pure ASGI middleware
- **What:** Rewrite RateLimitMiddleware and RequestLoggerMiddleware as pure ASGI middleware
- **Why:** BaseHTTPMiddleware has documented memory/connection issues in long-running apps. Mitigated by worker recycling but not eliminated.
- **Effort:** M → S with CC
- **Depends on:** Nothing
- **Added:** 2026-03-27 (CEO review of stability fix)
