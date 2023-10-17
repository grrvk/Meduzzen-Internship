import datetime
from pydantic import BaseModel


class ResultSchema(BaseModel):
    id: int
    user_id: int
    company_id: int
    quiz_id: int
    created_at: datetime.datetime
    result_right_count: int
    result_total_count: int


class ResultCreateRequest(BaseModel):
    user_id: int
    company_id: int
    quiz_id: int
    created_at: datetime.datetime
    result_right_count: int
    result_total_count: int
