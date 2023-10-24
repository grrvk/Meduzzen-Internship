import datetime
from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    Sent = "Sent"
    Read = "Read"


class NotificationSchema(BaseModel):
    id: int
    receiver_id: int
    status: Status
    created_at: datetime.datetime
    notification_data: str


class NotificationCreateSchema(BaseModel):
    receiver_id: int
    status: Status
    created_at: datetime.datetime
    notification_data: str


class NotificationDetailSchema(BaseModel):
    status: Status
    created_at: datetime.datetime
    notification_data: str
