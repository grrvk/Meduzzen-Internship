from app.models.model import Quiz
from app.schemas.actions import OwnerActionCreate, UserActionCreate
from app.schemas.user_answer import UserAnswerListSchema
from app.utils.repository import AbstractRepository
from fastapi import HTTPException


class ActionsValidator:
    def __init__(self, company_repo: AbstractRepository, users_repo: AbstractRepository,
                 invitations_repo: AbstractRepository, members_repo: AbstractRepository):
        self.company_repo: AbstractRepository = company_repo()
        self.users_repo: AbstractRepository = users_repo()
        self.invitations_repo: AbstractRepository = invitations_repo()
        self.members_repo: AbstractRepository = members_repo()

    async def owner_action_validation(self, action: OwnerActionCreate):
        company = await self.company_repo.get_one_by(id=action.company_id)
        if not company:
            raise HTTPException(status_code=400, detail="company with such id does not exists")
        if not await self.users_repo.get_one_by(id=action.user_id):
            raise HTTPException(status_code=400, detail="user with such id does not exists")
        return company

    async def user_action_validation(self, action: UserActionCreate):
        company = await self.company_repo.get_one_by(id=action.company_id)
        if not company:
            raise HTTPException(status_code=400, detail="company with such id does not exists")
        return company

    async def user_is_not_member(self, user_id: int, company_id: int):
        if await self.members_repo.get_one_by(user_id=user_id, company_id=company_id):
            raise HTTPException(status_code=400, detail="user is already a member")
        return True


class QuizzesDataValidator:
    def __init__(self, companies_repo: AbstractRepository, quizzes_repo: AbstractRepository,
                 questions_repo: AbstractRepository, answers_repo: AbstractRepository):
        self.company_repo: AbstractRepository = companies_repo()
        self.quizzes_repo: AbstractRepository = quizzes_repo()
        self.questions_repo: AbstractRepository = questions_repo()
        self.answers_repo: AbstractRepository = answers_repo()

    async def question_data_validation(self, company_id: int):
        company = await self.company_repo.get_one_by(id=company_id)
        if not company:
            raise HTTPException(status_code=400, detail="company with such id does not exists")
        return company

    def quiz_question_addition_check(self, quiz_dict: dict):
        questions = quiz_dict.get("questions")
        if len(questions) < 2:
            raise HTTPException(status_code=400, detail="not enough questions for quiz")
        for question in questions:
            self.question_answer_addition_check(question)
        return True

    def question_answer_addition_check(self, question_dict: dict):
        answers = question_dict.get("answers")
        if len(answers) < 2:
            raise HTTPException(status_code=400, detail="not enough answers for question")

        right_answer_exists = False
        for answer in answers:
            if answer.get("is_correct"):
                right_answer_exists = True
        if not right_answer_exists:
            raise HTTPException(status_code=400, detail="no right answer for the question")
        return True

    def question_dublicate_check(self, questions: dict):
        question_data_set = set(question.get("question_text") for question in questions)
        if len(question_data_set) != len(questions):
            raise HTTPException(status_code=400, detail="quiz contains identical questions")
        return True

    def answer_duplicate_check(self, questions: dict):
        for question in questions:
            q_answers = question.get("answers")
            answers_data_set = set(answer.get("answer_data") for answer in q_answers)
            if len(answers_data_set) != len(q_answers):
                raise HTTPException(status_code=400, detail="question contains identical answers")
        return True

    async def question_delete_check(self, quiz_id: int):
        questions = await self.questions_repo.get_all_by(quiz_id=quiz_id)
        if len(questions) < 3:
            raise HTTPException(status_code=400,
                                detail="after question delete quiz will contain less then two questions")
        return True

    async def answer_edit_check(self, question_id: int, is_correct: bool):
        right_answers = await self.answers_repo.get_all_by(question_id=question_id, is_correct=True)
        print(len(right_answers))
        print(is_correct)
        if len(right_answers) < 2 and not is_correct:
            raise HTTPException(status_code=400,
                                detail="after answer update question will not contain right answer")
        return True

    async def answer_delete_check(self, question_id: int):
        answers = await self.answers_repo.get_all_by(question_id=question_id)
        if len(answers) < 3:
            raise HTTPException(status_code=400,
                                detail="after answers delete question will contain less then two answers")
        return True

    async def question_existence_check(self, quiz_id: int, question_id: int):
        quiz = await self.quizzes_repo.get_one_by(id=quiz_id)
        if not quiz:
            raise HTTPException(status_code=400, detail="quiz with such id does not exists")
        question = await self.questions_repo.get_one_by(quiz_id=quiz_id, id=question_id)
        if not question:
            raise HTTPException(status_code=400, detail=f"such question does not exists for such quiz")
        return question

    async def answer_existence_check(self, quiz_id: int, question_id: int, answer_id: int):
        quiz = await self.quizzes_repo.get_one_by(id=quiz_id)
        if not quiz:
            raise HTTPException(status_code=400, detail="quiz with such id does not exists")
        question = await self.questions_repo.get_one_by(id=question_id, quiz_id=quiz_id)
        if not question:
            raise HTTPException(status_code=400, detail="question with such id does not exists")
        answer = await self.answers_repo.get_one_by(question_id=question_id, id=answer_id)
        if not answer:
            raise HTTPException(status_code=400, detail=f"such answer does not exists for such question")
        return answer, question


class ResultsDataValidator:
    def __init__(self, companies_repo: AbstractRepository, quizzes_repo: AbstractRepository,
                 questions_repo: AbstractRepository, answers_repo: AbstractRepository,
                 members_repo: AbstractRepository, users_repo: AbstractRepository):
        self.company_repo: AbstractRepository = companies_repo()
        self.quizzes_repo: AbstractRepository = quizzes_repo()
        self.questions_repo: AbstractRepository = questions_repo()
        self.answers_repo: AbstractRepository = answers_repo()
        self.members_repo: AbstractRepository = members_repo()
        self.users_repo: AbstractRepository = users_repo()

    async def answers_number_validator(self, user_answers: UserAnswerListSchema, quiz: Quiz):
        answers_questions_ids = set(answer.question_id for answer in user_answers.user_answers)
        quiz_questions_ids = set(question.id for question in quiz.questions)
        if answers_questions_ids != quiz_questions_ids:
            raise HTTPException(status_code=400, detail="not all questions have been answered")
        return True

    async def quiz_exist(self, company_id: int, quiz_id: int):
        quiz = await self.quizzes_repo.get_one_by(id=quiz_id, company_id=company_id)
        if not quiz:
            raise HTTPException(status_code=400, detail="no such quiz exist for the company")
        return quiz

    async def user_exists(self, user_id: int):
        if not await self.users_repo.get_one_by(id=user_id):
            raise HTTPException(status_code=400, detail="no such user")
        return True

    async def member_exist(self, member_id: int, company_id: int):
        user = await self.users_repo.get_one_by(id=member_id)
        company = await self.company_repo.get_one_by(id=company_id)
        if user.id == company.owner_id:
            return True
        member = await self.members_repo.get_one_by(user_id=member_id, company_id=company_id)
        if not member:
            return None
        return member

    async def has_created_quizzes(self, quizzes: list[Quiz]):
        if not quizzes:
            raise HTTPException(status_code=400, detail="user have not created any quizzes to get data from")
        return True



