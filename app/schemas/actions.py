from typing import Literal

from pydantic import BaseModel


class ActionSchema(BaseModel):
    id: int
    user_id: int
    company_id: int
    action: Literal['Send_invitation', 'Cancel_invitation', 'Accept_invitation', 'Deny_invitation',
                    'Send_request', 'Cancel_request', 'Accept_request', 'Deny_request',
                    'Leave_company', 'Delete_member']


class OwnerActionCreate(BaseModel):
    user_id: int
    company_id: int
    action: Literal['Send_invitation', 'Cancel_invitation', 'Accept_request', 'Deny_request', 'Delete_member',
                    'Add_admin', 'Remove_admin']


class UserActionCreate(BaseModel):
    company_id: int
    action: Literal['Send_request', 'Accept_invitation', 'Deny_invitation', 'Cancel_request', 'Leave_company']
