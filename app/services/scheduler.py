from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.dependencies import notifications_service

scheduler = AsyncIOScheduler()


async def send_notifications():
    notification_service = notifications_service()
    await notification_service.send_notifications()


scheduler.add_job(send_notifications, 'cron', hour=0)
