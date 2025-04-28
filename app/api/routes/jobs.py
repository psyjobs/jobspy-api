from fastapi import APIRouter, Depends, Query
from app.api.deps import get_api_key

router = APIRouter()

@router.get("/search_jobs")
async def search_jobs(
    api_key: str = Depends(get_api_key)
):
    pass