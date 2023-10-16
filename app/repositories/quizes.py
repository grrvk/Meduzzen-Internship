from app.models.model import Quiz
from app.utils.repository import SQLAlchemyRepository


class QuizzesRepository(SQLAlchemyRepository):
    model = Quiz
