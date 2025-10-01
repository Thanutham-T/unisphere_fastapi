from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere import models

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
        result = await session.execute(text("SELECT 1"))
        result.fetchall()

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Health check failed: {str(e)}") from e
    return {"status": "ok", "message": "Application is healthy"}
