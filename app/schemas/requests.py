from pydantic import BaseModel


class RequestSchema(BaseModel):
    id: int
    sender_id: int
    company_id: int
    is_accepted: bool | None


class RequestListResponse(BaseModel):
    sender_id: int
    company_id: int
