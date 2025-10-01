from abc import ABC, abstractmethod
from typing import List, Optional

from unisphere.schemas.branch_schema import (BranchCreateSchema, BranchSchema,
                                             BranchUpdateSchema)
from unisphere.schemas.branch_translation_schema import (
    BranchTranslationCreateSchema, BranchTranslationSchema,
    BranchTranslationUpdateSchema)


class BranchServiceInterface(ABC):
    # ==============================
    # Branch CRUD
    # ==============================
    
    @abstractmethod
    async def create_branch(self, data: BranchCreateSchema) -> BranchSchema:
        """Create a new branch"""
        pass

    @abstractmethod
    async def get_branch(self, branch_id: int) -> BranchSchema:
        """Get a branch by ID"""
        pass

    @abstractmethod
    async def update_branch(self, branch_id: int, data: BranchUpdateSchema) -> BranchSchema:
        """Update a branch by ID"""
        pass

    @abstractmethod
    async def delete_branch(self, branch_id: int) -> None:
        """Delete a branch by ID"""
        pass

    @abstractmethod
    async def list_branches(self, status: Optional[str] = None) -> List[BranchSchema]:
        """List all branches, optionally filtered by status"""
        pass

    # ==============================
    # Branch Translation CRUD
    # ==============================

    @abstractmethod
    async def create_translation(self, data: BranchTranslationCreateSchema) -> BranchTranslationSchema:
        """Create a translation for a branch"""
        pass

    @abstractmethod
    async def get_translation(self, branch_id: int, language_code: str) -> BranchTranslationSchema:
        """Get a branch translation by branch ID and language"""
        pass

    @abstractmethod
    async def update_translation(
        self, branch_id: int, language_code: str, data: BranchTranslationUpdateSchema
    ) -> BranchTranslationSchema:
        """Update a branch translation"""
        pass

    @abstractmethod
    async def delete_translation(self, branch_id: int, language_code: str) -> None:
        """Delete a branch translation"""
        pass

    @abstractmethod
    async def list_translations(self, branch_id: int) -> List[BranchTranslationSchema]:
        """List all translations for a branch"""
        pass
