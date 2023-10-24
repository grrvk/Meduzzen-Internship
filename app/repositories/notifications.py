from app.models.model import Notification
from app.utils.repository import SQLAlchemyRepository


class NotificationsRepository(SQLAlchemyRepository):
    model = Notification
