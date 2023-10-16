from fastapi import HTTPException

from app.models.model import User
from app.schemas.answers import AnswerCreateRequest
from app.schemas.questions import QuestionCreateRequest
from app.schemas.quizzes import QuizCreateRequest
from app.services.permissions import QuizzesPermissions
from app.utils.repository import AbstractRepository
from app.utils.validations import QuizzesDataValidator


class QuizzesService:
    def __init__(self, companies_repo: AbstractRepository, quizzes_repo: AbstractRepository,
                 questions_repo: AbstractRepository, answers_repo: AbstractRepository,
                 members_repo: AbstractRepository):
        self.quizzes_repo: AbstractRepository = quizzes_repo()
        self.questions_repo: AbstractRepository = questions_repo()
        self.answers_repo: AbstractRepository = answers_repo()
        self.companies_repo: AbstractRepository = companies_repo()

        self.quizzes_permissions = QuizzesPermissions(members_repo)
        self.validator = QuizzesDataValidator(companies_repo, quizzes_repo, questions_repo, answers_repo)

    async def get_all_quizzes(self, company_id: int, current_user: User):
        company = await self.validator.question_data_validation(company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        return await self.quizzes_repo.get_all_by(company_id=company_id)

    async def add_quiz(self, quiz: QuizCreateRequest, current_user: User):
        company = await self.validator.question_data_validation(quiz.company_id)
        quiz_check = await self.quizzes_repo.get_all_by(company_id=company.id, quiz_name=quiz.quiz_name)
        if quiz_check:
            raise HTTPException(status_code=400, detail=f"such quiz already exists")
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        quiz_dict = quiz.model_dump()
        await self.validator.question_addition_check(quiz_dict)

        quiz_data = {"quiz_name": quiz_dict.get("quiz_name"), "quiz_title": quiz_dict.get("quiz_title"),
                     "quiz_description": quiz_dict.get("quiz_description"), "created_by": current_user.id,
                     "updated_by": current_user.id, "company_id": quiz_dict.get("company_id")}

        quiz_id = await self.quizzes_repo.create_one(quiz_data)

        questions = quiz_dict.get("questions")
        for question in questions:
            question_data = {"quiz_id": quiz_id, "created_by": current_user.id, "updated_by": current_user.id,
                             "question_text": question.get("question_text"), "company_id": quiz_dict.get("company_id")}
            question_id = await self.questions_repo.create_one(question_data)

            answers = question.get("answers")
            for answer in answers:
                answer.update({"question_id": question_id})
                await self.answers_repo.create_one(answer)

        return quiz_id

    async def delete_quiz(self, quiz_id: int, current_user: User):
        quiz_check = await self.quizzes_repo.get_one_by(id=quiz_id)
        if not quiz_check:
            raise HTTPException(status_code=400, detail=f"such quiz does not exists")
        company = await self.validator.question_data_validation(quiz_check.company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        await self.quizzes_repo.delete_one(quiz_id)

        return True