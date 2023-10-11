from fastapi import HTTPException

from app.models.model import User
from app.schemas.companies import CompanyCreateRequest, CompanyUpdateRequest
from app.services.permissions import CompaniesPermissions
from app.utils.repository import AbstractRepository


class CompaniesService:
    def __init__(self, companies_repo: AbstractRepository):
        self.companies_repo: AbstractRepository = companies_repo()
        self.permission_service = CompaniesPermissions()

    async def add_company(self, company: CompanyCreateRequest, current_user: User):
        if await self.companies_repo.get_one_by(company_name=company.company_name):
            raise HTTPException(status_code=400, detail="company with such name already exists")
        company_dict = company.model_dump(exclude_unset=True)
        company_dict.update({"owner_id": current_user.id})
        company_id = await self.companies_repo.create_one(company_dict)
        return company_id

    async def get_all_companies(self):
        return await self.companies_repo.get_all()

    async def get_company_by_id(self, company_id: int):
        company = await self.companies_repo.get_one_by(id=company_id)
        if not company:
            raise HTTPException(status_code=400, detail="no company with such id")
        return company

    async def edit_company(self, id: int, data: CompanyUpdateRequest, current_user: User):
        company = await self.companies_repo.get_one_by(id=id)
        if not company:
            raise HTTPException(status_code=400, detail="no company with such id")
        company_dict = data.model_dump(exclude_unset=True)
        await self.permission_service.can_update_company(company.owner_id, current_user, company_dict)
        return await self.companies_repo.update_one(id, company_dict)

    async def delete_company(self, id: int, current_user: User):
        company = await self.companies_repo.get_one_by(id=id)
        if not company:
            raise HTTPException(status_code=400, detail="no company with such id")
        await self.permission_service.can_delete_company(company.owner_id, current_user)
        await self.companies_repo.delete_one(id)
        return True
