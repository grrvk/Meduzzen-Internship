from app.models.model import Result
from app.utils.repository import SQLAlchemyRepository


class ResultsRepository(SQLAlchemyRepository):
    model = Result
