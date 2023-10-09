from fastapi import APIRouter, Depends
from typing import Annotated

from starlette import status

from app.auth.utils_auth import check_token
from app.schemas.response import Response
from app.schemas.schema import UserSignUpRequest, UserUpdateRequest, UsersListResponse, UserSchema
from app.services.auth import AuthService
from app.services.dependencies import users_service, authentication_service
from app.services.users import UsersService

router = APIRouter()


@router.post("/add_user", response_model=Response[int])
async def add_user(
        user: UserSignUpRequest,
        user_service: Annotated[UsersService, Depends(users_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await user_service.add_user(user, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="added",
        result=res
    )


@router.put("/users/{user_id}", response_model=Response[int])
async def update_user(
        user_id: int,
        user: UserUpdateRequest,
        user_service: Annotated[UsersService, Depends(users_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await user_service.edit_user(user_id, user, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="updated",
        result=res
    )


@router.delete("/users/{user_id}", response_model=Response[int])
async def delete_user(
        user_id: int,
        user_service: Annotated[UsersService, Depends(users_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await user_service.delete_user(user_id, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="OK",
        result=res
    )


@router.get("/users", response_model=list[UsersListResponse])
async def get_all_users(
        user_service: Annotated[UsersService, Depends(users_service)]
):
    return await user_service.get_all_users()


@router.get("/users/{user_id}", response_model=Response[UserSchema])
async def read_item(
        user_id: int,
        user_service: Annotated[UsersService, Depends(users_service)]
):
    res = await user_service.get_user_by_id(user_id)
    return Response(
            status_code=status.HTTP_200_OK,
            detail="OK",
            result=res
        )

