from pydantic import BaseModel


class UserAnswerSchema(BaseModel):
    question_id: int
    answer_data: str


class UserAnswerListSchema(BaseModel):
    user_answers: list[UserAnswerSchema]
