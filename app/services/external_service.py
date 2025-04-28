import uuid
import time
import httpx
from app.core.logging_config import get_logger

logger = get_logger("services.external_service")


async def fetch_data_from_external_api(url: str, params: dict = None):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    logger.debug(f"External API request {request_id} started: GET {url} - Params: {params}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        elapsed_time = time.time() - start_time
        logger.debug(
            f"External API request {request_id} completed: GET {url} - "
            f"Status: {response.status_code} - Time: {elapsed_time:.3f}s"
        )
        
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        elapsed_time = time.time() - start_time
        logger.error(
            f"External API request {request_id} failed with status {e.response.status_code}: "
            f"GET {url} - Time: {elapsed_time:.3f}s - Response: {e.response.text}"
        )
        raise
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.exception(
            f"External API request {request_id} failed: GET {url} - "
            f"Time: {elapsed_time:.3f}s - Error: {str(e)}"
        )
        raise