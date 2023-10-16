from app.schemas.actions import OwnerActionCreate, UserActionCreate
from app.utils.repository import AbstractRepository
from fastapi import HTTPException


class ActionsValidator:
    def __init__(self, company_repo: AbstractRepository, users_repo: AbstractRepository,
                 invitations_repo: AbstractRepository, members_repo: AbstractRepository):
        self.company_repo: AbstractRepository = company_repo()
        self.users_repo: AbstractRepository = users_repo()
        self.invitations_repo: AbstractRepository = invitations_repo()
        self.members_repo: AbstractRepository = members_repo()

    async def owner_action_validation(self, action: OwnerActionCreate):
        company = await self.company_repo.get_one_by(id=action.company_id)
        if not company:
            raise HTTPException(status_code=400, detail="company with such id does not exists")
        if not await self.users_repo.get_one_by(id=action.user_id):
            raise HTTPException(status_code=400, detail="user with such id does not exists")
        return company

    async def user_action_validation(self, action: UserActionCreate):
        company = await self.company_repo.get_one_by(id=action.company_id)
        if not company:
            raise HTTPException(status_code=400, detail="company with such id does not exists")
        return company

    async def user_is_not_member(self, user_id: int, company_id: int):
        if not await self.members_repo.get_one_by(user_id=user_id, company_id=company_id):
            return True
        raise HTTPException(status_code=400, detail="user is already a member")
        if await self.members_repo.get_one_by(user_id=user_id, company_id=company_id):
            raise HTTPException(status_code=400, detail="user is already a member")
        return True



