import datetime

from fastapi import HTTPException

from app.models.model import User
from app.schemas.answers import AnswerCreateRequest, AnswerUpdateRequest
from app.schemas.questions import QuestionCreateRequest, QuestionUpdateRequest
from app.schemas.quizzes import QuizCreateRequest, QuizUpdateRequest
from app.services.notifications import NotificationsService
from app.services.permissions import QuizzesPermissions
from app.utils.repository import AbstractRepository
from app.utils.validations import QuizzesDataValidator


class QuizzesService:
    def __init__(self, companies_repo: AbstractRepository, quizzes_repo: AbstractRepository,
                 questions_repo: AbstractRepository, answers_repo: AbstractRepository,
                 members_repo: AbstractRepository, notifications_repo: AbstractRepository,
                 results_repo: AbstractRepository):
        self.quizzes_repo: AbstractRepository = quizzes_repo()
        self.questions_repo: AbstractRepository = questions_repo()
        self.answers_repo: AbstractRepository = answers_repo()
        self.companies_repo: AbstractRepository = companies_repo()
        self.members_repo: AbstractRepository = members_repo()

        self.notifications = NotificationsService(members_repo, notifications_repo, quizzes_repo, results_repo)
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
        self.validator.quiz_question_addition_check(quiz_dict)

        quiz_data = {"quiz_name": quiz_dict.get("quiz_name"), "quiz_title": quiz_dict.get("quiz_title"),
                     "quiz_description": quiz_dict.get("quiz_description"), "created_at": datetime.datetime.utcnow(),
                     "created_by": current_user.id, "updated_by": current_user.id,
                     "quiz_frequency": quiz_dict.get("quiz_frequency"), "company_id": quiz_dict.get("company_id")}
        questions = quiz_dict.get("questions")

        self.validator.question_dublicate_check(questions)
        self.validator.answer_duplicate_check(questions)

        quiz_id = await self.quizzes_repo.create_one(quiz_data)
        await self.notifications.create_notification(quiz_id, int(quiz_dict.get("company_id")))

        for question in questions:
            question_data = {"quiz_id": quiz_id, "created_by": current_user.id, "updated_by": current_user.id,
                             "question_text": question.get("question_text"), "company_id": quiz_dict.get("company_id")}
            question_id = await self.questions_repo.create_one(question_data)

            answers = question.get("answers")
            for answer in answers:
                answer.update({"question_id": question_id,  "created_by": current_user.id,
                               "updated_by": current_user.id})
                await self.answers_repo.create_one(answer)

        return quiz_id

    async def delete_quiz(self, quiz_id: int, current_user: User):
        quiz = await self.quizzes_repo.get_one_by(id=quiz_id)
        if not quiz:
            raise HTTPException(status_code=400, detail=f"such quiz does not exists")
        company = await self.validator.question_data_validation(quiz.company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        await self.quizzes_repo.delete_one(quiz_id)
        return True

    async def edit_quiz(self, quiz_id: int, data: QuizUpdateRequest, current_user: User):
        quiz = await self.quizzes_repo.get_one_by(id=quiz_id)
        if not quiz:
            raise HTTPException(status_code=400, detail=f"such quiz does not exists")
        company = await self.companies_repo.get_one_by(id=quiz.company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        quiz_dict = data.model_dump(exclude_unset=True)
        quiz_dict.update({"updated_by": current_user.id})
        await self.quizzes_repo.update_one(quiz_id, quiz_dict)
        return True

    async def add_question(self, quiz_id: int, data: QuestionCreateRequest, current_user: User):
        quiz = await self.quizzes_repo.get_one_by(id=quiz_id)
        if not quiz:
            raise HTTPException(status_code=400, detail=f"such quiz does not exists")
        company = await self.companies_repo.get_one_by(id=quiz.company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        question_dict = data.model_dump()
        if await self.questions_repo.get_one_by(quiz_id=quiz_id, question_text=question_dict.get("question_text")):
            raise HTTPException(status_code=400, detail=f"such question is already in quiz")
        self.validator.question_answer_addition_check(question_dict)

        question = {"question_text": question_dict.get("question_text"), "quiz_id": quiz_id,
                    "created_by": current_user.id, "updated_by": current_user.id, "company_id": quiz.company_id}
        question_id = await self.questions_repo.create_one(question)

        answers = question_dict.get("answers")
        for answer in answers:
            answer.update({"question_id": question_id, "created_by": current_user.id, "updated_by": current_user.id})
            await self.answers_repo.create_one(answer)

        return question_id

    async def edit_question(self, quiz_id: int, question_id: int, data: QuestionUpdateRequest, current_user: User):
        question = await self.validator.question_existence_check(quiz_id, question_id)
        company = await self.companies_repo.get_one_by(id=question.company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        question_dict = data.model_dump(exclude_unset=True)
        question_dict.update({"updated_by": current_user.id})
        await self.questions_repo.update_one(question_id, question_dict)
        return True

    async def delete_question(self, quiz_id: int, question_id: int, current_user: User):
        question = await self.validator.question_existence_check(quiz_id, question_id)
        company = await self.companies_repo.get_one_by(id=question.company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)
        await self.validator.question_delete_check(quiz_id)

        await self.questions_repo.delete_one(question_id)
        return True

    async def add_answer(self, quiz_id: int, question_id: int, data: AnswerCreateRequest, current_user: User):
        question = await self.validator.question_existence_check(quiz_id, question_id)
        company = await self.companies_repo.get_one_by(id=question.company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        answer_dict = data.model_dump()
        if await self.answers_repo.get_one_by(question_id=question_id, answer_data=answer_dict.get("answer_data")):
            raise HTTPException(status_code=400, detail=f"such answer is already in question")
        answer_dict.update({"question_id": question_id, "created_by": current_user.id, "updated_by": current_user.id})
        return await self.answers_repo.create_one(answer_dict)

    async def edit_answer(self, quiz_id: int, question_id: int, answer_id: int,
                          data: AnswerUpdateRequest, current_user: User):
        answer, question = await self.validator.answer_existence_check(quiz_id, question_id, answer_id)
        company = await self.companies_repo.get_one_by(id=question.company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        answer_dict = data.model_dump(exclude_unset=True)
        if "is_correct" in answer_dict:
            await self.validator.answer_edit_check(question_id, answer_dict.get("is_correct"))
        answer_dict.update({"updated_by": current_user.id})
        await self.answers_repo.update_one(answer_id, answer_dict)
        return True

    async def delete_answer(self, quiz_id: int, question_id: int, answer_id: int, current_user: User):
        answer, question = await self.validator.answer_existence_check(quiz_id, question_id, answer_id)
        company = await self.companies_repo.get_one_by(id=question.company_id)
        await self.quizzes_permissions.has_user_permissions(company, current_user)

        await self.validator.answer_delete_check(question_id)

        await self.answers_repo.delete_one(answer_id)
        return True