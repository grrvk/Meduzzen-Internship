import datetime

from fastapi import APIRouter, Depends
from typing import Annotated
from starlette import status
from app.auth.utils_auth import check_token
from app.schemas.notifications import NotificationDetailSchema
from app.schemas.response import Response
from app.services.auth import AuthService
from app.services.dependencies import authentication_service, notifications_service
from app.services.notifications import NotificationsService
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = APIRouter(tags=["notifications"])
scheduler = AsyncIOScheduler()


async def send_notifications():
    notification_service = notifications_service()
    await notification_service.send_notifications()


scheduler.add_job(send_notifications, 'cron', hour=0)


@router.get("/notifications", response_model=list[NotificationDetailSchema])
async def get_notifications(
        notification_service: Annotated[NotificationsService, Depends(notifications_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    return await notification_service.get_notification(current_user)


@router.post("/notifications/{notification_id}", response_model=Response[int])
async def read_notification(
        notification_id: int,
        notification_service: Annotated[NotificationsService, Depends(notifications_service)],
        auth_service: Annotated[AuthService, Depends(authentication_service)],
        payload: Annotated[dict, Depends(check_token)],
):
    current_user = await auth_service.get_user_by_payload(payload)
    res = await notification_service.read_notification(notification_id, current_user)
    return Response(
            status_code=status.HTTP_200_OK,
            detail="OK",
            result=res
        )
