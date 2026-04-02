from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from lms_backend.database import get_session

router = APIRouter()

@router.get("/")
async def list_items(session: AsyncSession = Depends(get_session)):
    try:
        from lms_backend.db.items import read_items
        items = await read_items(session)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
