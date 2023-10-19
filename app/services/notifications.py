import datetime

from fastapi import HTTPException

from app.models.model import User
from app.schemas.answers import AnswerCreateRequest, AnswerUpdateRequest
from app.schemas.notifications import NotificationCreateSchema
from app.schemas.questions import QuestionCreateRequest, QuestionUpdateRequest
from app.schemas.quizzes import QuizCreateRequest, QuizUpdateRequest
from app.services.permissions import QuizzesPermissions, NotificationsPermissions
from app.utils.repository import AbstractRepository
from app.utils.validations import QuizzesDataValidator


class NotificationsService:
    def __init__(self, members_repo: AbstractRepository, notifications_repo: AbstractRepository,
                 quizzes_repo: AbstractRepository, results_repo: AbstractRepository):
        self.members_repo: AbstractRepository = members_repo()
        self.notifications_repo: AbstractRepository = notifications_repo()
        self.quizzes_repo: AbstractRepository = quizzes_repo()
        self.results_repo: AbstractRepository = results_repo()

        self.permissions = NotificationsPermissions(notifications_repo)

    async def create_notification(self, quiz_id: int, company_id: int):
        members = await self.members_repo.get_all_by(company_id=company_id)
        for member in members:
            data = NotificationCreateSchema(receiver_id=member.user_id, status="Sent",
                                            notification_data=f"Created new quiz {quiz_id}",
                                            created_at=datetime.datetime.utcnow())
            await self.notifications_repo.create_one(data.__dict__)
        return True

    async def read_notification(self, notification_id: int, current_user: User):
        notification = await self.permissions.can_answer_notification(notification_id, current_user.id)
        notification_dict = {"status": "Read"}
        return await self.notifications_repo.update_one(notification.id, notification_dict)

    async def get_notification(self, current_user: User):
        return await self.notifications_repo.get_all_by(receiver_id=current_user.id, status="Sent")

    async def send_notifications(self):
        members = await self.members_repo.get_all()
        for member in members:
            quizzes = await self.quizzes_repo.get_all_by(company_id=member.company_id)
            for quiz in quizzes:
                result = await self.results_repo.get_one_by(user_id=member.user_id, quiz_id=quiz.id)
                if result is None or (result.created_at-quiz.created_at)/quiz.quiz_frequency >= 1:
                    data = NotificationCreateSchema(receiver_id=member.user_id, status="Sent",
                                                    notification_data=f"Ypu can pass quiz {quiz.id}",
                                                    created_at=datetime.datetime.utcnow())
                    await self.notifications_repo.create_one(data.__dict__)
        return True
