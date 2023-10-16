from enum import Enum
from typing import Literal

from pydantic import BaseModel


class Actions(str, Enum):
    Send_invitation = "Send_invitation"
    Cancel_invitation = "Cancel_invitation"
    Accept_request = "Accept_request"
    Deny_request = "Deny_request"
    Delete_member = "Delete_member"
    Send_request = "Send_request"
    Accept_invitation = "Accept_invitation"
    Deny_invitation = "Deny_invitation"
    Cancel_request = "Cancel_request"
    Leave_company = "Leave_company"
    Add_admin = "Add_admin"
    Remove_admin = "Remove_admin"


class ActionSchema(BaseModel):
    id: int
    user_id: int
    company_id: int
    action: Actions


class OwnerActions(str, Enum):
    Send_invitation = "Send_invitation"
    Cancel_invitation = "Cancel_invitation"
    Accept_request = "Accept_request"
    Deny_request = "Deny_request"
    Delete_member = "Delete_member"
    Add_admin = "Add_admin"
    Remove_admin = "Remove_admin"


class OwnerActionCreate(BaseModel):
    user_id: int
    company_id: int
    action: OwnerActions


class UserActions(str, Enum):
    Send_request = "Send_request"
    Accept_invitation = "Accept_invitation"
    Deny_invitation = "Deny_invitation"
    Cancel_request = "Cancel_request"
    Leave_company = "Leave_company"


class UserActionCreate(BaseModel):
    company_id: int
    action: UserActions
