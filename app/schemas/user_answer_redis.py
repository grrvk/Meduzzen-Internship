from pydantic import BaseModel


class AnswerData(BaseModel):
    user_id: int
    company_id: int
    quiz_id: int
    question_id: int
    answer_data: str
    is_correct: int


class AnswerDataDetail(BaseModel):
    company_id: int
    quiz_id: int
    question_id: int
    answer_data: str
    is_correct: int
