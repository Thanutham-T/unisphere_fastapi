from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# User schemas
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    profile_image_url: Optional[str] = None
    role: str = "user"


# Registration schemas - แบ่งเป็น 3 ส่วน
class PersonalInfoCreate(BaseModel):
    """ส่วนที่ 1: ข้อมูลส่วนตัว"""
    first_name: str
    last_name: str
    phone_number: Optional[str] = None


class EducationInfoCreate(BaseModel):
    """ส่วนที่ 2: ข้อมูลการศึกษา"""
    student_id: Optional[str] = None
    education_level: Optional[str] = None  # dropdown
    campus: Optional[str] = None  # dropdown
    faculty: Optional[str] = None  # dropdown
    major: Optional[str] = None  # dropdown
    curriculum: Optional[str] = None  # textfield
    department: Optional[str] = None  # textfield


class AccountInfoCreate(BaseModel):
    """ส่วนที่ 3: ข้อมูลยืนยัน"""
    email: EmailStr
    password: str
    confirm_password: str


class UserRegister(BaseModel):
    """รวมข้อมูลทั้ง 3 ส่วน"""
    personal_info: PersonalInfoCreate
    education_info: EducationInfoCreate
    account_info: AccountInfoCreate


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    student_id: Optional[str] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    password: str
    role: str = "user"

    # Education information
    faculty: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    curriculum: Optional[str] = None
    education_level: Optional[str] = None
    campus: Optional[str] = None


class UserUpdate(BaseModel):
    student_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    profile_image_url: Optional[str] = None
    role: Optional[str] = None

    # Education information
    faculty: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    curriculum: Optional[str] = None
    education_level: Optional[str] = None
    campus: Optional[str] = None


class User(UserBase):
    id: int
    student_id: Optional[str] = None
    faculty: Optional[str] = None
    department: Optional[str] = None
    major: Optional[str] = None
    curriculum: Optional[str] = None
    education_level: Optional[str] = None
    campus: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Personal info for step 1 registration


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None


class UserResponse(BaseModel):
    """Response after successful login/register"""
    user: User
    token: Token

    @classmethod
    def from_db_user(cls, db_user, token: Token):
        """Create UserResponse from database User model"""
        user_dict = {
            "id": db_user.id,
            "student_id": db_user.student_id,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name,
            "email": db_user.email,
            "phone_number": db_user.phone_number,
            "profile_image_url": db_user.profile_image_url,
            "role": db_user.role,
            "is_active": db_user.is_active,
            "faculty": db_user.faculty,
            "department": db_user.department,
            "major": db_user.major,
            "curriculum": db_user.curriculum,
            "education_level": db_user.education_level,
            "campus": db_user.campus,
            "created_at": db_user.created_at,
            "updated_at": db_user.updated_at,
        }
        user = User(**user_dict)
        return cls(user=user, token=token)
