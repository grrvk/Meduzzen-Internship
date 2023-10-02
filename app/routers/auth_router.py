from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Response, status
from typing import Annotated

from app.auth.dependencies import get_current_user
from app.auth.utils_auth import VerifyToken
from app.models.model import User
from app.schemas.schema import Token
from app.services.dependencies import users_service
from app.services.users import UserService
from app.auth.jwt import create_access_token
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()
router = APIRouter()


@router.post("/token", response_model=Token)
async def login(
        user_service: Annotated[UserService, Depends(users_service)],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user_db = await user_service.authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(
        data={"sub": user_db.user_email}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get('/me')
async def get_me(
        user: Annotated[User, Depends(get_current_user)]):
    return user


@router.get("/me/auth0")
async def get_me(
        response: Response,
        token: Annotated[str, Depends(token_auth_scheme)]
):
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    return result


@router.get('/private')
async def get_private():
    pass
