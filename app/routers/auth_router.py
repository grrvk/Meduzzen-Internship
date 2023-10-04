from fastapi import APIRouter, Depends
from typing import Annotated
from app.auth.utils_auth import check_token, get_user_by_payload
from app.schemas.schema import Token, UserSignInRequest
from app.services.dependencies import users_service
from app.services.users import UserService
from app.auth.jwt import create_access_token
from fastapi.security import HTTPBearer

token_auth_scheme = HTTPBearer()
router = APIRouter()


@router.post("/token", response_model=Token)
async def login(
        user_service: Annotated[UserService, Depends(users_service)],
        user: UserSignInRequest,
):
    user_db = await user_service.authenticate_user(user.user_email, user.hashed_password)
    access_token = create_access_token(
        data={"sub": user_db.user_email}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
async def get_me(
        payload: Annotated[dict, Depends(check_token)],
        user_service: Annotated[UserService, Depends(users_service)]
):
    user_id = await get_user_by_payload(payload, user_service)
    return {
        "status_code": 200,
        "data": user_id,
        "details": None
    }




