from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models import get_session  # your AsyncSession dependency
from unisphere.schemas.branch_schema import (BranchCreateSchema, BranchSchema,
                                             BranchUpdateSchema)
from unisphere.schemas.branch_translation_schema import (
    BranchTranslationCreateSchema, BranchTranslationSchema,
    BranchTranslationUpdateSchema)
from unisphere.services.branch_service.DBBranchService import DBBranchService

router = APIRouter(prefix="/branches", tags=["branches"])

# Dependency
async def get_branch_service(session: AsyncSession = Depends(get_session)) -> DBBranchService:
    return DBBranchService(session)


# ==============================
# Branch Endpoints
# ==============================
@router.post("/", response_model=BranchSchema, status_code=status.HTTP_201_CREATED)
async def create_branch(data: BranchCreateSchema, service: DBBranchService = Depends(get_branch_service)):
    return await service.create_branch(data)


@router.get("/{branch_id}", response_model=BranchSchema)
async def get_branch(branch_id: int, service: DBBranchService = Depends(get_branch_service)):
    return await service.get_branch(branch_id)


@router.put("/{branch_id}", response_model=BranchSchema)
async def update_branch(branch_id: int, data: BranchUpdateSchema, service: DBBranchService = Depends(get_branch_service)):
    return await service.update_branch(branch_id, data)


@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_branch(branch_id: int, service: DBBranchService = Depends(get_branch_service)):
    await service.delete_branch(branch_id)
    return None


@router.get("/", response_model=List[BranchSchema])
async def list_branches(status: Optional[str] = None, service: DBBranchService = Depends(get_branch_service)):
    return await service.list_branches(status=status)


# ==============================
# Branch Translation Endpoints
# ==============================
@router.post("/{branch_id}/translations", response_model=BranchTranslationSchema, status_code=status.HTTP_201_CREATED)
async def create_translation(branch_id: int, data: BranchTranslationCreateSchema, service: DBBranchService = Depends(get_branch_service)):
    return await service.create_translation(data)


@router.get("/{branch_id}/translations/{language_code}", response_model=BranchTranslationSchema)
async def get_translation(branch_id: int, language_code: str, service: DBBranchService = Depends(get_branch_service)):
    return await service.get_translation(branch_id, language_code)


@router.put("/{branch_id}/translations/{language_code}", response_model=BranchTranslationSchema)
async def update_translation(branch_id: int, language_code: str, data: BranchTranslationUpdateSchema, service: DBBranchService = Depends(get_branch_service)):
    return await service.update_translation(branch_id, language_code, data)


@router.delete("/{branch_id}/translations/{language_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_translation(branch_id: int, language_code: str, service: DBBranchService = Depends(get_branch_service)):
    await service.delete_translation(branch_id, language_code)
    return None


@router.get("/{branch_id}/translations", response_model=List[BranchTranslationSchema])
async def list_translations(branch_id: int, service: DBBranchService = Depends(get_branch_service)):
    return await service.list_translations(branch_id)
