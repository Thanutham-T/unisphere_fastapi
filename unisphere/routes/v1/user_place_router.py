from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session
from unisphere.schemas.user_place_schema import (UserPlaceCreate,
                                                 UserPlaceListResponse,
                                                 UserPlaceResponse)
from unisphere.services.user_place_service.DBUserPlaceService import \
    DBUserPlaceService

from .auth_router import get_current_user

router = APIRouter(prefix="/user-places", tags=["user-places"])


def get_user_place_service(session: AsyncSession = Depends(get_session)) -> DBUserPlaceService:
    return DBUserPlaceService(session)


@router.post("/", response_model=UserPlaceResponse, status_code=status.HTTP_201_CREATED)
async def save_place_to_collection(
    payload: UserPlaceCreate,
    service: DBUserPlaceService = Depends(get_user_place_service),
    current_user=Depends(get_current_user),
):
    try:
        return await service.create_place(payload, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=UserPlaceListResponse)
async def get_my_places(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: DBUserPlaceService = Depends(get_user_place_service),
    current_user=Depends(get_current_user),
):
    places, total = await service.list_my_places(user_id=current_user.id, limit=limit, offset=offset)
    return UserPlaceListResponse(places=places, total=total, limit=limit, offset=offset)


@router.delete("/{place_id}")
async def delete_place(place_id: int, service: DBUserPlaceService = Depends(get_user_place_service), current_user=Depends(get_current_user)):
    ok = await service.delete_place(place_id, user_id=current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Place not found")
    return {"message": "Place removed from collection successfully"}
