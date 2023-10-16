from app.models.model import Member
from app.utils.repository import SQLAlchemyRepository


class MembersRepository(SQLAlchemyRepository):
    model = Member
