from typing import Optional

from pydantic import BaseModel

#from app.models.model import Answer
from app.schemas.answers import AnswerCreateRequest, AnswerSchema, AnswerDetailsSchema


class QuestionSchema(BaseModel):
    id: int
    question_text: str
    quiz_id: int
    company_id: int
    created_by: int
    updated_by: int
    answers: list[AnswerSchema]


class QuestionDetailsSchema(BaseModel):
    question_text: str
    answers: list[AnswerDetailsSchema]


class QuestionCreateRequest(BaseModel):
    question_text: str
    answers: list[AnswerCreateRequest]


class QuestionUpdateRequest(BaseModel):
    question_text: Optional[str] = None
