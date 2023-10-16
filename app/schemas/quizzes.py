import datetime
from pydantic import BaseModel, field_validator

from app.schemas.questions import QuestionSchema, QuestionCreateRequest


class QuizSchema(BaseModel):
    id: int
    quiz_name: str
    quiz_title: str
    quiz_description: str
    quiz_frequency: int | None
    created_by: int
    updated_by: int
    company_id: int
    last_passed_at: datetime.datetime
    #questions: list[QuestionSchema]


class QuizCreateRequest(BaseModel):
    quiz_name: str
    quiz_title: str
    quiz_description: str
    company_id: int
    questions: list[QuestionCreateRequest]
