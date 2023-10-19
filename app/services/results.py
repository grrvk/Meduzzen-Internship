import asyncio
import datetime
import csv
import json

from fastapi import HTTPException
from redis import Redis

from app.models.model import User
from app.schemas.result import ResultCreateRequest
from app.schemas.user_answer import UserAnswerSchema, UserAnswerListSchema
from app.schemas.user_answer_redis import AnswerData, AnswerDataDetail
from app.services.permissions import QuizzesPermissions, ResultsPermissions
from app.services.redis import RedisService
from app.utils.repository import AbstractRepository
from app.utils.validations import ResultsDataValidator


class ResultsService:
    def __init__(self, companies_repo: AbstractRepository, quizzes_repo: AbstractRepository,
                 questions_repo: AbstractRepository, answers_repo: AbstractRepository,
                 results_repo: AbstractRepository, members_repo: AbstractRepository,
                 users_repo: AbstractRepository):
        self.quizzes_repo: AbstractRepository = quizzes_repo()
        self.questions_repo: AbstractRepository = questions_repo()
        self.answers_repo: AbstractRepository = answers_repo()
        self.results_repo: AbstractRepository = results_repo()

        self.validator = ResultsDataValidator(companies_repo, quizzes_repo, questions_repo, answers_repo,
                                              members_repo, users_repo)
        self.permissions = ResultsPermissions(companies_repo, members_repo)
        self.redis_service = RedisService()

    async def get_result(self, company_id: int, quiz_id: int, user_answers: UserAnswerListSchema, current_user: User,
                         redis_client: Redis):
        quiz = await self.validator.quiz_exist(company_id, quiz_id)
        await self.validator.answers_number_validator(user_answers, quiz)
        if quiz.last_passed_at is None or quiz.last_passed_at.weekday() != datetime.datetime.utcnow().weekday():
            quiz_dict = {"last_passed_at": datetime.datetime.utcnow(), "quiz_frequency": quiz.quiz_frequency + 1}
            await self.quizzes_repo.update_one(quiz_id, quiz_dict)

        correct_results = 0
        for answer in user_answers.user_answers:
            question = await self.questions_repo.get_one_by(id=answer.question_id, quiz_id=quiz.id)
            check_answer = await self.answers_repo.get_one_by(question_id=question.id, answer_data=answer.answer_data)
            is_answer_correct = 0
            if check_answer and check_answer.is_correct:
                correct_results += 1
                is_answer_correct = 1
            redis_answer_data = AnswerData(user_id=current_user.id, company_id=company_id, quiz_id=quiz_id,
                                           question_id=question.id, answer_data=answer.answer_data,
                                           is_correct=is_answer_correct)
            await self.redis_service.save_result_to_redis(redis_client, redis_answer_data)

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

    async def get_results(self, current_user: User, redis_client: Redis):
        answers = []
        async for key in redis_client.scan_iter(f"answer:{current_user.id}:*"):
            data = await self.redis_service.get_result_from_redis(redis_client, key)
            answer = AnswerDataDetail(company_id=data.get("company_id"), quiz_id=data.get("quiz_id"),
                                      question_id=data.get("question_id"), answer_data=data.get("answer_data"),
                                      is_correct=data.get("is_correct"))
            answers.append(answer)
        return answers

    async def get_results_for_user(self, current_user: User, user_id: int, redis_client: Redis):
        quizzes = await self.quizzes_repo.get_all_by(created_by=current_user.id)
        await self.validator.has_created_quizzes(quizzes)
        await self.validator.user_exists(user_id)

        answers = []
        for quiz in quizzes:
            async for key in redis_client.scan_iter(f"answer:{user_id}:{quiz.company_id}:{quiz.id}:*"):
                data = await self.redis_service.get_result_from_redis(redis_client, key)
                if await self.validator.member_exist(user_id, quiz.company_id):
                    answer = AnswerDataDetail(company_id=data.get("company_id"), quiz_id=data.get("quiz_id"),
                                              question_id=data.get("question_id"), answer_data=data.get("answer_data"),
                                              is_correct=data.get("is_correct"))
                    answers.append(answer)
        return answers

    async def get_all_results_for_company(self, current_user: User, company_id: int, redis_client: Redis):
        await self.permissions.has_user_permissions(company_id, current_user)
        answers = []
        async for key in redis_client.scan_iter(f"answer:*:{company_id}:*:*"):
            data = await self.redis_service.get_result_from_redis(redis_client, key)
            if await self.validator.member_exist(int(data.get("user_id")), company_id):
                answer = AnswerData(user_id=data.get("user_id"), company_id=data.get("company_id"),
                                    quiz_id=data.get("quiz_id"), question_id=data.get("question_id"),
                                    answer_data=data.get("answer_data"), is_correct=data.get("is_correct"))
                answers.append(answer)
        return answers

    async def export_to_csv(self, redis_client: Redis, current_user: User):
        with open('results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            field = ["quiz", "question", "answer", "is_correct"]
            writer.writerow(field)

            async for key in redis_client.scan_iter(f"answer:{current_user.id}:*"):
                data = await self.redis_service.get_result_from_redis(redis_client, key)
                filtered_data = [data.get("quiz_id"), data.get("question_id"), data.get("answer_data"),
                                 data.get("is_correct")]
                writer.writerow(filtered_data)
        return True

    async def export_to_json(self, redis_client: Redis, current_user: User):
        with open("results.json", "w") as outfile:
            async for key in redis_client.scan_iter(f"answer:{current_user.id}:*"):
                data = await self.redis_service.get_result_from_redis(redis_client, key)
                filtered_data = {"quiz": data.get("quiz_id"), "question": data.get("question_id"),
                                 "answer_data": data.get("answer_data"),
                                 "is_correct": data.get("is_correct")}
                json.dump(filtered_data, outfile)
        return True
      
