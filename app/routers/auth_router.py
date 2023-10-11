from fastapi import APIRouter, Depends
from typing import Annotated

from starlette import status

from app.auth.utils_auth import check_token
from app.schemas.response import Response
from app.schemas.schema import Token, UserSignInRequest
from app.services.auth import AuthService
from app.services.dependencies import authentication_service
from fastapi.security import HTTPBearer


token_auth_scheme = HTTPBearer()
router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
async def login(
        user: UserSignInRequest,
        auth_service: Annotated[AuthService, Depends(authentication_service)]
):
    return await auth_service.authenticate_user(user.user_email, user.hashed_password)


@router.get("/me", response_model=Response[int])
async def get_me(
        payload: Annotated[dict, Depends(check_token)],
        auth_service: Annotated[AuthService, Depends(authentication_service)]

):
    res = await auth_service.get_user_by_payload(payload)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="OK",
        result=res.id
    )




