import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.schemas.answers import AnswerSchema, AnswerCreateRequest


class QuestionSchema(BaseModel):
    id: int
    question_text: str
    quiz_id: int
    company_id: int
    created_by: int
    updated_by: int
    #answers: list[AnswerCreateRequest]


class QuestionCreateRequest(BaseModel):
    question_text: str
    answers: list[AnswerCreateRequest]
