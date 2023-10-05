from app.models.model import User
from app.utils.repository import SQLAlchemyRepository


class AuthRepository(SQLAlchemyRepository):
    model = User
    