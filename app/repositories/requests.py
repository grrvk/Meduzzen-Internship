from app.models.model import Request
from app.utils.repository import SQLAlchemyRepository


class RequestsRepository(SQLAlchemyRepository):
    model = Request
