# Frequently Asked Questions

Q: How do I enable Swagger UI?  
A: Set `ENABLE_SWAGGER_UI=true` in your `.env` or Compose file.

Q: Where are logs stored?  
A: By default in the `logs/` directory of the container.

Q: How can I customize default search parameters?  
A: Use environment variables like `DEFAULT_DISTANCE`, `DEFAULT_RESULTS_WANTED`.

Q: How do I debug env var issues?  
A: Run `python scripts/check_env.py` or inspect `/config-sources` endpoint.
