from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.dependencies import get_db
from app.core.logging_config import get_logger

logger = get_logger("api.endpoints.example")

router = APIRouter()

@router.get("/items/")
async def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.debug(f"Fetching items with skip={skip}, limit={limit}")
    try:
        items = crud.get_items(db, skip=skip, limit=limit)
        logger.debug(f"Successfully retrieved {len(items)} items")
        return items
    except Exception as e:
        logger.exception(f"Error retrieving items: {str(e)}")
        raise

@router.post("/items/")
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    logger.debug(f"Creating new item: {item.dict()}")
    try:
        db_item = crud.create_item(db=db, item=item)
        logger.info(f"Successfully created item with id: {db_item.id}")
        return db_item
    except Exception as e:
        logger.exception(f"Error creating item: {str(e)}")
        raise