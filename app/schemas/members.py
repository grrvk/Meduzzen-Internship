from typing import Literal

from pydantic import BaseModel


class MemberSchema(BaseModel):
    id: int
    user_id: int
    role: Literal['member', 'admin']
    company_id: int


class MemberCreate(BaseModel):
    user_id: int
    role: Literal['member', 'admin']
    company_id: int
