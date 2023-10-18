from app.models.model import Answer
from app.utils.repository import SQLAlchemyRepository


class AnswersRepository(SQLAlchemyRepository):
    model = Answer
