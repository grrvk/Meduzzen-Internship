import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    id: int
    user_email: str
    hashed_password: str
    user_firstname: str
    user_lastname: str
    user_status: Optional[bool] = None
    user_city: Optional[str] = None
    user_phone: Optional[str] = None
    user_avatar: Optional[str] = None


class UserSignUpRequest(BaseModel):
    user_email: str
    user_firstname: str
    user_lastname: str
    hashed_password: str
    user_status: Optional[bool] = None
    user_city: Optional[str] = None
    user_phone: Optional[str] = None
    user_avatar: Optional[str] = None
    is_superuser: Optional[bool] = False
    created_at: Optional[datetime.datetime] = None

    @field_validator('hashed_password')
    def name_must_contain_space(cls, p):
        if not p:
            raise ValueError('Password cannot be blank')
        return p.title()


class UserSignInRequest(BaseModel):
    user_email: str
    hashed_password: str


class UserUpdateRequest(BaseModel):
    hashed_password: Optional[str] = None
    user_email: Optional[str] = None
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None
    user_status: Optional[bool] = None
    user_city: Optional[str] = None
    user_phone: Optional[str] = None
    user_avatar: Optional[str] = None
    is_superuser: Optional[bool] = None
    updated_at: Optional[datetime.datetime] = None


class UsersListResponse(BaseModel):
    user_firstname: str
    user_lastname: str


class UserDetailResponse(BaseModel):
    user_city: str
    user_phone: str
    user_avatar: str
    is_superuser: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
