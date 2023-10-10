from typing import Optional

from pydantic import BaseModel


class CompanySchema(BaseModel):
    id: int
    owner_id: int
    company_name: str
    company_title: str
    company_description: str
    company_city: str
    company_phone: str
    company_links: Optional[str] = None
    company_avatar: Optional[str] = None
    is_visible: bool


class CompanyCreateRequest(BaseModel):
    company_name: str
    company_title: str
    company_description: Optional[str] = None
    company_city: Optional[str] = None
    company_phone: Optional[str] = None
    company_links: Optional[str] = None
    company_avatar: Optional[str] = None
    is_visible: bool


class CompanyUpdateRequest(BaseModel):
    company_name: Optional[str] = None
    company_title: Optional[str] = None
    company_description: Optional[str] = None
    company_city: Optional[str] = None
    company_phone: Optional[str] = None
    company_links: Optional[str] = None
    company_avatar: Optional[str] = None
    is_visible: Optional[bool] = None


class CompaniesListResponse(BaseModel):
    company_name: str
    company_description: str
