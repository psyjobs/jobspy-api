"""Background job processing for JobSpy Docker API."""
import asyncio
from typing import Dict, Any, Optional
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Simple in-memory job storage (would use a database in production)
jobs = {}

async def process_job_async(job_id: str, search_function, params: Dict[str, Any]):
    """Process a job asynchronously."""
    try:
        logger.info(f"Starting background job {job_id}")
        jobs[job_id]["status"] = "running"
        
        # Execute the search
        result, is_cached = await asyncio.to_thread(search_function, params)
        
        # Store result
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
        jobs[job_id]["is_cached"] = is_cached
        jobs[job_id]["completed_at"] = datetime.now().isoformat()
        
        logger.info(f"Completed background job {job_id}")
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

def create_background_job(search_function, params: Dict[str, Any]) -> str:
    """Create a new background job."""
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "id": job_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "params": params,
    }
    
    # Start the background task
    asyncio.create_task(process_job_async(job_id, search_function, params))
    
    return job_id

def get_job_status(job_id: str) -> Optional[Dict[str, Any]]:
    """Get the status of a job."""
    return jobs.get(job_id)
