import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class AnswerSchema(BaseModel):
    id: int
    answer_data: str
    is_correct: bool
    question_id: int
    created_by: int
    updated_by: int


class AnswerDetailsSchema(BaseModel):
    answer_data: str
    is_correct: bool
    created_by: int
    updated_by: int


class AnswerCreateRequest(BaseModel):
    answer_data: str
    is_correct: bool


class AnswerUpdateRequest(BaseModel):
    answer_data: Optional[str] = None
    is_correct: Optional[bool] = False
