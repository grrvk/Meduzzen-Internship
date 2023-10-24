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


class ResultDetailSchema(BaseModel):
    company_id: int
    quiz_id: int
    result_right_count: int
    result_total_count: int


class ResultListSchema(BaseModel):
    results: list[ResultDetailSchema]


class AverageResultListDetail(BaseModel):
    company_id: int
    quiz_id: int
    average_result: float


class CompanyAverageResultForUserListDetail(BaseModel):
    user_id: int
    company_id: int
    quiz_id: int
    average_result: float


class UserAverageResultDateListDetail(BaseModel):
    company_id: int
    quiz_id: int
    average_result: int
    created_at: datetime.datetime


class UserPassingDateListDetail(BaseModel):
    user_id: int
    last_passed_at: datetime.datetime
