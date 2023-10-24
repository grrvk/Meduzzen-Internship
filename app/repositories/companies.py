from app.models.model import Company
from app.utils.repository import SQLAlchemyRepository


class CompaniesRepository(SQLAlchemyRepository):
    model = Company
