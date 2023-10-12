from app.models.model import Invitation
from app.utils.repository import SQLAlchemyRepository


class InvitationsRepository(SQLAlchemyRepository):
    model = Invitation
