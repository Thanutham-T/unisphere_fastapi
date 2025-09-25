from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.dependencies import get_db, verify_password, create_access_token, create_refresh_token, get_current_user_id, blacklist_token, get_token_from_credentials
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, Token, LogoutResponse
from app.models.user_model import User
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.student_id == user_data.student_id)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or student ID already exists"
        )
    
    # Create new user
    from app.core.dependencies import get_password_hash
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        student_id=user_data.student_id,
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        faculty=user_data.faculty,
        year=user_data.year,
        profile_image_url=user_data.profile_image_url,
        role=user_data.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return access tokens"""
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.student_id == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Get current user profile"""
    user = db.query(User).filter(User.id == current_user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/logout", response_model=LogoutResponse)
async def logout(token: str = Depends(get_token_from_credentials), current_user_id: int = Depends(get_current_user_id)):
    """Logout user by blacklisting the token"""
    # Add token to blacklist
    blacklist_token(token)
    
    return LogoutResponse(
        message="Successfully logged out",
        success=True
    )


@router.get("/health")
async def auth_health():
    """Auth service health check"""
    return {"status": "healthy", "service": "authentication"}