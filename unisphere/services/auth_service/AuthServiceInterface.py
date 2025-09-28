from abc import ABC, abstractmethod
from typing import Optional

from unisphere.models.user_model import User
from unisphere.schemas.user_schema import UserCreate, UserLogin, UserResponse


class AuthServiceInterface(ABC):
    """Interface for authentication service"""

    @abstractmethod
    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user"""
        pass

    @abstractmethod
    async def login_user(self, login_data: UserLogin) -> UserResponse:
        """Login user"""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass

    @abstractmethod
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        pass

    @abstractmethod
    async def create_tokens(self, user: User) -> dict:
        """Create access and refresh tokens"""
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token"""
        pass
