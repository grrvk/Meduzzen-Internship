import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.schemas.questions import QuestionSchema, QuestionCreateRequest, QuestionDetailsSchema


class QuizSchema(BaseModel):
    id: int
    quiz_name: str
    quiz_title: str
    quiz_description: str
    quiz_frequency: int | None
    created_by: int
    updated_by: int
    company_id: int
    last_passed_at: datetime.datetime | None
    questions: list[QuestionSchema]


class QuizDetailsSchema(BaseModel):
    quiz_name: str
    quiz_title: str
    quiz_description: str
    quiz_frequency: int | None
    created_by: int
    updated_by: int
    company_id: int
    last_passed_at: datetime.datetime | None
    questions: list[QuestionDetailsSchema]


class QuizCreateRequest(BaseModel):
    quiz_name: str
    quiz_title: str
    quiz_description: str
    company_id: int
    questions: list[QuestionCreateRequest]


class QuizUpdateRequest(BaseModel):
    quiz_name: Optional[str] = None
    quiz_title: Optional[str] = None
    quiz_description: Optional[str] = None


class QuizDateRequest(BaseModel):
    quiz_name: str
    last_passed_at: datetime.datetime | None

