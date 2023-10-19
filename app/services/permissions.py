from fastapi import HTTPException
from fastapi.security import HTTPBearer

from app.models.model import User, Company
from app.utils.repository import AbstractRepository

security = HTTPBearer()


class UserPermissions:
    def __init__(self):
        self.permission_error = HTTPException(status_code=403, detail="Not enough permissions")

    async def can_update_user(self, id: int, current_user: User, user_payload: dict) -> bool:
        if current_user.is_superuser:
            return True
        if current_user.id != id:
            raise self.permission_error
        for key in user_payload.keys():
            if key != "user_firstname" and key != "user_lastname" and key != "hashed_password":
                raise self.permission_error
        return True

    async def can_delete_user(self, id: int, current_user: User) -> bool:
        if current_user.id == id or current_user.is_superuser:
            return True
        raise self.permission_error

    async def can_add_user(self, current_user: User):
        if current_user.is_superuser:
            return True
        raise self.permission_error


class CompaniesPermissions:
    def __init__(self):
        self.permission_error = HTTPException(status_code=403, detail="Not enough permissions")

    async def can_update_company(self, owner_id: int, current_user: User, company_payload: dict) -> bool:
        if current_user.is_superuser:
            return True
        if current_user.id != owner_id:
            raise self.permission_error
        for key in company_payload.keys():
            if key != "company_name" and key != "company_description":
                raise self.permission_error
        return True

    async def can_delete_company(self, owner_id: int, current_user: User) -> bool:
        if current_user.id == owner_id or current_user.is_superuser:
            return True
        raise self.permission_error


class ActionsPermissions:
    def __init__(self):
        self.permission_error = HTTPException(status_code=403, detail="Not enough permissions")

    async def is_user_owner(self, company: Company, current_user: User) -> bool:
        if current_user.id != company.owner_id:
            raise self.permission_error
        return True


class QuizzesPermissions:
    def __init__(self, members_repo: AbstractRepository):
        self.permission_error = HTTPException(status_code=403, detail="Not enough permissions")
        self.members_repo: AbstractRepository = members_repo()

    async def has_user_permissions(self, company: Company, current_user: User):
        if current_user.id == company.owner_id:
            return True
        member = await self.members_repo.get_one_by(user_id=current_user.id, company_id=company.id)
        if not member or member.role == "member":
            raise self.permission_error
        return True


class ResultsPermissions:
    def __init__(self, companies_repo: AbstractRepository, members_repo: AbstractRepository):
        self.permission_error = HTTPException(status_code=403, detail="Not enough permissions")
        self.companies_repo: AbstractRepository = companies_repo()
        self.members_repo: AbstractRepository = members_repo()

    async def has_user_permissions(self, company_id: int, current_user: User):
        company = await self.companies_repo.get_one_by(id=company_id)
        if current_user.id == company.owner_id:
            return True
        member = await self.members_repo.get_one_by(user_id=current_user.id, company_id=company.id)
        if not member or member.role == "member":
            raise self.permission_error
        return True


    async def user_owner_or_admin(self, company_id: int, current_user: User):
        company = await self.companies_repo.get_one_by(id=company_id)
        if current_user.id == company.owner_id:
            return True
        member = await self.members_repo.get_one_by(user_id=current_user.id, company_id=company.id)
        if not member or member.role == "member":
            return None
        return True



