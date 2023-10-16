import datetime
from pydantic import BaseModel, field_validator


class AnswerSchema(BaseModel):
    id: int
    answer_data: str
    is_correct: bool
    question_id: int


class AnswerCreateRequest(BaseModel):
    answer_data: str
    is_correct: bool
