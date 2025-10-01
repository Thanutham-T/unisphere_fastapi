from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.models.branch_model import BranchModel, BranchTranslationModel
from unisphere.schemas.branch_schema import (BranchCreateSchema, BranchSchema,
                                             BranchUpdateSchema)
from unisphere.schemas.branch_translation_schema import (
    BranchTranslationCreateSchema, BranchTranslationSchema,
    BranchTranslationUpdateSchema)

from .BranchServiceInterface import BranchServiceInterface


class DBBranchService(BranchServiceInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    # ==============================
    # Branch CRUD
    # ==============================
    async def create_branch(self, data: BranchCreateSchema) -> BranchSchema:
        branch = BranchModel.from_orm(data)
        self.session.add(branch)
        await self.session.commit()
        await self.session.refresh(branch)
        return BranchSchema.from_orm(branch)

    async def get_branch(self, branch_id: int) -> BranchSchema:
        branch = await self.session.get(BranchModel, branch_id)
        if not branch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")
        return BranchSchema.from_orm(branch)

    async def update_branch(self, branch_id: int, data: BranchUpdateSchema) -> BranchSchema:
        branch = await self.session.get(BranchModel, branch_id)
        if not branch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(branch, field, value)

        self.session.add(branch)
        await self.session.commit()
        await self.session.refresh(branch)
        return BranchSchema.from_orm(branch)

    async def delete_branch(self, branch_id: int) -> None:
        branch = await self.session.get(BranchModel, branch_id)
        if not branch:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")

        await self.session.delete(branch)
        await self.session.commit()

    async def list_branches(self, status: Optional[str] = None) -> List[BranchSchema]:
        query = select(BranchModel)
        if status:
            query = query.where(BranchModel.status == status)

        result = await self.session.execute(query)
        branches = result.scalars().all()
        return [BranchSchema.from_orm(branch) for branch in branches]

    # ==============================
    # Branch Translation CRUD
    # ==============================
    async def create_translation(self, data: BranchTranslationCreateSchema) -> BranchTranslationSchema:
        translation = BranchTranslationModel.from_orm(data)
        self.session.add(translation)
        await self.session.commit()
        await self.session.refresh(translation)
        return BranchTranslationSchema.from_orm(translation)

    async def get_translation(self, branch_id: int, language_code: str) -> BranchTranslationSchema:
        query = select(BranchTranslationModel).where(
            BranchTranslationModel.branch_id == branch_id,
            BranchTranslationModel.language_code == language_code
        )
        result = await self.session.execute(query)
        translation = result.scalar_one_or_none()
        if not translation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found")
        return BranchTranslationSchema.from_orm(translation)

    async def update_translation(
        self, branch_id: int, language_code: str, data: BranchTranslationUpdateSchema
    ) -> BranchTranslationSchema:
        query = select(BranchTranslationModel).where(
            BranchTranslationModel.branch_id == branch_id,
            BranchTranslationModel.language_code == language_code
        )
        result = await self.session.execute(query)
        translation = result.scalar_one_or_none()
        if not translation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found")

        for field, value in data.dict(exclude_unset=True).items():
            setattr(translation, field, value)

        self.session.add(translation)
        await self.session.commit()
        await self.session.refresh(translation)
        return BranchTranslationSchema.from_orm(translation)

    async def delete_translation(self, branch_id: int, language_code: str) -> None:
        query = select(BranchTranslationModel).where(
            BranchTranslationModel.branch_id == branch_id,
            BranchTranslationModel.language_code == language_code
        )
        result = await self.session.execute(query)
        translation = result.scalar_one_or_none()
        if not translation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Translation not found")

        await self.session.delete(translation)
        await self.session.commit()

    async def list_translations(self, branch_id: int) -> List[BranchTranslationSchema]:
        query = select(BranchTranslationModel).where(BranchTranslationModel.branch_id == branch_id)
        result = await self.session.execute(query)
        translations = result.scalars().all()
        return [BranchTranslationSchema.from_orm(t) for t in translations]
