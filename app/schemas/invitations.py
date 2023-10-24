from pydantic import BaseModel


class InvitationSchema(BaseModel):
    id: int
    sender_id: int
    user_id: int
    company_id: int
    is_accepted: bool | None


class InvitationListResponse(BaseModel):
    sender_id: int
    user_id: int
    company_id: int
