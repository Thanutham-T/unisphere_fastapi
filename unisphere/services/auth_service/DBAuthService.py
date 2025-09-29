from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.core.config import get_settings
from unisphere.models.user_model import User
from unisphere.schemas.user_schema import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)
from unisphere.services.auth_service.AuthServiceInterface import AuthServiceInterface


class DBAuthService(AuthServiceInterface):
    """Database implementation of authentication service"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.settings = get_settings()

    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        statement = select(User).where(User.id == user_id)
        result = await self.session.exec(statement)
        return result.first()

    async def create_tokens(self, user: User) -> dict:
        """Create access and refresh tokens"""
        # Access token
        access_token_expires = timedelta(
            minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + access_token_expires,
            "type": "access"
        }
        access_token = jwt.encode(
            access_token_payload,
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM
        )

        # Refresh token
        refresh_token_expires = timedelta(
            minutes=self.settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + refresh_token_expires,
            "type": "refresh"
        }
        refresh_token = jwt.encode(
            refresh_token_payload,
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash password
        hashed_password = self._hash_password(user_data.password)

        # Create user
        db_user = User(
            student_id=user_data.student_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            password_hash=hashed_password,
            role=user_data.role,
            faculty=user_data.faculty,
            department=user_data.department,
            major=user_data.major,
            curriculum=user_data.curriculum,
            education_level=user_data.education_level,
            campus=user_data.campus,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)

        # Create tokens
        tokens = await self.create_tokens(db_user)
        token = Token(**tokens)

        return UserResponse.from_db_user(db_user, token)

    async def login_user(self, login_data: UserLogin) -> UserResponse:
        """Login user"""
        # Get user by email
        user = await self.get_user_by_email(login_data.email)
        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        if not await self.verify_password(login_data.password, user.password_hash):
            raise ValueError("Invalid email or password")

        # Check if user is active
        if not user.is_active:
            raise ValueError("User account is inactive")

        # Update last login time
        user.updated_at = datetime.now()
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        # Create tokens
        tokens = await self.create_tokens(user)
        token = Token(**tokens)

        return UserResponse.from_db_user(user, token)

    async def update_user_profile(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user profile"""
        try:
            # Get user from database
            stmt = select(User).where(User.id == user_id)
            result = await self.session.exec(stmt)
            user = result.first()

            if not user:
                return None

            # Update only provided fields
            update_data = user_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)

            # Update timestamp
            user.updated_at = datetime.now()

            # Save to database
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

            return user

        except Exception as e:
            await self.session.rollback()
            print(f"Error updating user profile: {e}")
            return None
