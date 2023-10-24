import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from app.schemas.questions import QuestionSchema, QuestionCreateRequest, QuestionDetailsSchema


class QuizSchema(BaseModel):
    id: int
    quiz_name: str
    quiz_title: str
    quiz_description: str
    quiz_frequency: int
    created_at: datetime.datetime
    created_by: int
    updated_by: int
    company_id: int
    last_passed_at: datetime.datetime | None
    questions: list[QuestionSchema]


class QuizDetailsSchema(BaseModel):
    quiz_name: str
    quiz_title: str
    quiz_description: str
    quiz_frequency: int
    created_at: datetime.datetime
    created_by: int
    updated_by: int
    company_id: int
    last_passed_at: datetime.datetime | None
    questions: list[QuestionDetailsSchema]


class QuizCreateRequest(BaseModel):
    quiz_name: str
    quiz_title: str
    quiz_description: str
    quiz_frequency: int
    company_id: int
    questions: list[QuestionCreateRequest]

    @field_validator('quiz_frequency')
    def frequency_validation(cls, quiz_frequency):
        if quiz_frequency <= 0:
            raise ValueError('Frequency must be greater than zero')
        return quiz_frequency


class QuizUpdateRequest(BaseModel):
    quiz_name: Optional[str] = None
    quiz_title: Optional[str] = None
    quiz_description: Optional[str] = None


class QuizDateRequest(BaseModel):
    quiz_name: str
    last_passed_at: datetime.datetime | None

