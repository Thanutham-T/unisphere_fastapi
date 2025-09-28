from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from unisphere.core.config import get_settings
from unisphere.models import get_session
from unisphere.schemas.user_schema import User as SchemaUser
from unisphere.schemas.user_schema import (UserCreate, UserLogin, UserRegister,
                                           UserResponse)
from unisphere.services.auth_service.AuthServiceInterface import \
    AuthServiceInterface
from unisphere.services.auth_service.DBAuthService import DBAuthService
from unisphere.services.auth_service.MockAuthService import MockAuthService

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


# Dependency to get auth service (mock or DB)
def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthServiceInterface:
    settings = get_settings()
    if settings.USE_MOCK:
        return MockAuthService()
    return DBAuthService(session=session)


# Dependency to get current user from token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthServiceInterface = Depends(get_auth_service)
) -> SchemaUser:
    """Get current authenticated user"""
    token = credentials.credentials

    # Verify token
    payload = await auth_service.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user_id = int(user_id_str)
    user = await auth_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return SchemaUser.model_validate(user)


@router.post(
    "/register",
    summary="Register a new user",
    description="Register a new user with personal info, education info, and account credentials",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_register: UserRegister,
    auth_service: AuthServiceInterface = Depends(get_auth_service)
):
    """Register a new user"""
    try:
        # Validate password confirmation
        if user_register.account_info.password != user_register.account_info.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and confirm password do not match"
            )

        # Create user data from registration info
        user_create = UserCreate(
            # Personal info
            first_name=user_register.personal_info.first_name,
            last_name=user_register.personal_info.last_name,
            phone_number=user_register.personal_info.phone_number,

            # Education info
            student_id=user_register.education_info.student_id,
            education_level=user_register.education_info.education_level,
            campus=user_register.education_info.campus,
            faculty=user_register.education_info.faculty,
            major=user_register.education_info.major,
            curriculum=user_register.education_info.curriculum,
            department=user_register.education_info.department,

            # Account info
            email=user_register.account_info.email,
            password=user_register.account_info.password
        )

        return await auth_service.register_user(user_create)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e


@router.post(
    "/login",
    summary="Login user",
    description="Login user with email and password",
    response_model=UserResponse
)
async def login_user(
    login_data: UserLogin,
    auth_service: AuthServiceInterface = Depends(get_auth_service)
):
    """Login user"""
    try:
        return await auth_service.login_user(login_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        ) from e


@router.post(
    "/logout",
    summary="Logout user",
    description="Logout current user (client-side token invalidation)"
)
async def logout_user():
    """Logout user (client should delete the token)"""
    return {"message": "Successfully logged out"}


@router.get(
    "/me",
    summary="Get current user",
    description="Get current authenticated user information",
    response_model=SchemaUser
)
async def get_me(current_user: SchemaUser = Depends(get_current_user)):
    """Get current user information"""
    return current_user


# Endpoint สำหรับ Flutter dropdowns
@router.get(
    "/education-options",
    summary="Get education options",
    description="Get available options for education dropdowns"
)
async def get_education_options():
    """Get education options for dropdowns"""
    return {
        "education_levels": [
            "ปริญญาตรี",
            "ปริญญาโท",
            "ปริญญาเอก",
            "อนุปริญญา"
        ],
        "campuses": [
            "วิทยาเขตกรุงเทพมหานคร",
            "วิทยาเขตรังสิต",
            "วิทยาเขตสารสนเทศ",
            "วิทยาเขตศิลปกรรมศาสตร์"
        ],
        "faculties": [
            "คณะวิศวกรรมศาสตร์",
            "คณะแพทยศาสตร์",
            "คณะเศรษฐศาสตร์",
            "คณะบริหารธุรกิจ",
            "คณะวิทยาศาสตร์",
            "คณะนิติศาสตร์",
            "คณะสถาปัตยกรรมศาสตร์",
            "คณะศิลปกรรมศาสตร์"
        ],
        "majors": {
            "คณะวิศวกรรมศาสตร์": [
                "วิศวกรรมคอมพิวเตอร์",
                "วิศวกรรมไฟฟ้า",
                "วิศวกรรมเครื่องกล",
                "วิศวกรรมโยธา"
            ],
            "คณะแพทยศาสตร์": [
                "แพทยศาสตร์",
                "พยาบาลศาสตร์",
                "เทคนิคการแพทย์"
            ],
            "คณะเศรษฐศาสตร์": [
                "เศรษฐศาสตร์",
                "เศรษฐศาสตร์ธุรกิจ"
            ],
            "คณะบริหารธุรกิจ": [
                "บริหารธุรกิจ",
                "การบัญชี",
                "การตลาด"
            ]
        }
    }
