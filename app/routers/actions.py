from fastapi import APIRouter, Depends
from typing import Annotated

from starlette import status

from app.auth.utils_auth import check_token
from app.schemas.actions import OwnerActionCreate, UserActionCreate
from app.schemas.invitations import InvitationListResponse
from app.schemas.members import MemberListResponse
from app.schemas.requests import RequestListResponse
from app.schemas.response import Response

from app.services.owner_actions import OwnerActionHandler
from app.services.auth import AuthService
from app.services.dependencies import authentication_service, owner_actions_handler, user_actions_handler
from app.services.user_actions import UserActionHandler

router = APIRouter(tags=["actions"])


@router.post("/owner-action", response_model=Response[int])
async def create_owner_action(
        action: OwnerActionCreate,
        action_handler: Annotated[OwnerActionHandler, Depends(owner_actions_handler)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await action_handler.handle_action(action, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="OK",
        result=res
    )


@router.post("/user-action", response_model=Response[int])
async def create_user_action(
        action: UserActionCreate,
        action_handler: Annotated[UserActionHandler, Depends(user_actions_handler)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await action_handler.handle_action(action, current_user)
    return Response(
        status_code=status.HTTP_200_OK,
        detail="OK",
        result=res
    )


@router.post("/invitations", response_model=list[InvitationListResponse])
async def get_user_invitations(
        action_handler: Annotated[UserActionHandler, Depends(user_actions_handler)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await action_handler.get_all_invitations(current_user)


@router.post("/requests", response_model=list[RequestListResponse])
async def get_user_requests(
        action_handler: Annotated[UserActionHandler, Depends(user_actions_handler)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await action_handler.get_all_requests(current_user)


@router.post("/invitations/{company_id}", response_model=list[InvitationListResponse])
async def get_invitations_for_company(
        company_id: int,
        action_handler: Annotated[OwnerActionHandler, Depends(owner_actions_handler)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await action_handler.get_all_invitations(company_id, current_user)



@router.post("/requests/{company_id}", response_model=list[RequestListResponse])
async def get_requests_for_company(
        company_id: int,
        action_handler: Annotated[OwnerActionHandler, Depends(owner_actions_handler)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await action_handler.get_all_requests(company_id, current_user)



