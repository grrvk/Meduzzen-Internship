import datetime

from fastapi import HTTPException

from app.models.model import User
from app.schemas.result import ResultCreateRequest
from app.schemas.user_answer import UserAnswerSchema, UserAnswerListSchema
from app.services.permissions import QuizzesPermissions
from app.utils.repository import AbstractRepository
from app.utils.validations import ResultsDataValidator


class ResultsService:
    def __init__(self, companies_repo: AbstractRepository, quizzes_repo: AbstractRepository,
                 questions_repo: AbstractRepository, answers_repo: AbstractRepository,
                 results_repo: AbstractRepository):
        self.quizzes_repo: AbstractRepository = quizzes_repo()
        self.questions_repo: AbstractRepository = questions_repo()
        self.answers_repo: AbstractRepository = answers_repo()
        self.results_repo: AbstractRepository = results_repo()
        self.validator = ResultsDataValidator(companies_repo, quizzes_repo, questions_repo, answers_repo)

    async def get_result(self, company_id: int, quiz_id: int, user_answers: UserAnswerListSchema, current_user: User):
        quiz = await self.validator.quiz_exist(company_id, quiz_id)
        if quiz.last_passed_at is None or quiz.last_passed_at.weekday() != datetime.datetime.utcnow().weekday():
            quiz_dict = {"last_passed_at": datetime.datetime.utcnow(), "quiz_frequency": quiz.quiz_frequency + 1}
            await self.quizzes_repo.update_one(quiz_id, quiz_dict)

        correct_results = 0
        for answer in user_answers.user_answers:
            question = await self.questions_repo.get_one_by(id=answer.question_id, quiz_id=quiz.id)
            if question:
                check_answer = await self.answers_repo.get_one_by(question_id=question.id, answer_data=answer.answer_data)
                if check_answer and check_answer.is_correct:
                    correct_results += 1

        result = await self.results_repo.get_one_by(user_id=current_user.id, company_id=company_id, quiz_id=quiz_id)
        result_dict = {"result_right_count": correct_results, "result_total_count": len(quiz.questions)}
        if result:
            await self.results_repo.update_one(result.id, result_dict)
            return result.id

        result_dict.update({"user_id": current_user.id, "company_id": company_id, "quiz_id": quiz_id})
        return await self.results_repo.create_one(result_dict)

    async def get_average_in_company(self, company_id: int, current_user: User):
        results = await self.results_repo.get_all_by(company_id=company_id, user_id=current_user.id)
        right_answers_count = 0
        total_answers_count = 0
        for result in results:
            right_answers_count += result.result_right_count
            total_answers_count += result.result_total_count

        if total_answers_count == 0:
            return 0
        return round(float(right_answers_count / total_answers_count), 4)

    async def get_average_total(self, current_user: User):
        results = await self.results_repo.get_all_by(user_id=current_user.id)
        right_answers_count = 0
        total_answers_count = 0
        for result in results:
            right_answers_count += result.result_right_count
            total_answers_count += result.result_total_count

        if total_answers_count == 0:
            return 0
        return round(float(right_answers_count / total_answers_count), 4)
