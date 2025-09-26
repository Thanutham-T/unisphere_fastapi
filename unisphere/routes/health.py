from fastapi import APIRouter, Depends
from fastapi import HTTPException
from unisphere import models
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text


router = APIRouter(prefix="/health")


@router.get(
    "",
    summary="Health Check",
    description="Check the health status of the application.",
)
async def health_check(
    session: AsyncSession = Depends(models.get_session),
) -> dict[str, str]:
    try:
        q = await session.exec(text("SELECT 1"))
        q.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
    return {"status": "ok", "message": "Application is healthy"}