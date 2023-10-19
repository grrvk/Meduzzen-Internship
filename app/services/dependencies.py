from app.repositories.users import UsersRepository
from .notifications import NotificationsService
from .owner_actions import OwnerActionHandler
from .auth import AuthService
from .companies import CompaniesService
from .permissions import UserPermissions
from .quizzes import QuizzesService
from .results import ResultsService
from .user_actions import UserActionHandler
from .users import UsersService
from app.repositories.auth import AuthRepository
from ..repositories.answers import AnswersRepository
from ..repositories.companies import CompaniesRepository
from ..repositories.members import MembersRepository
from ..repositories.notifications import NotificationsRepository
from ..repositories.questions import QuestionsRepository
from ..repositories.quizes import QuizzesRepository
from ..repositories.results import ResultsRepository


def users_service():
    return UsersService(UsersRepository)


def authentication_service():
    return AuthService(AuthRepository)


def companies_service():
    return CompaniesService(CompaniesRepository)


def quizzes_service():
    return QuizzesService(CompaniesRepository, QuizzesRepository, QuestionsRepository,
                          AnswersRepository, MembersRepository, NotificationsRepository, ResultsRepository)


def results_service():
    return ResultsService(CompaniesRepository, QuizzesRepository, QuestionsRepository,
                          AnswersRepository, ResultsRepository, MembersRepository,
                          UsersRepository)


def notifications_service():
    return NotificationsService(MembersRepository, NotificationsRepository, QuizzesRepository, ResultsRepository)


def permissions_service():
    return UserPermissions()


def owner_actions_handler():
    return OwnerActionHandler()


def user_actions_handler():
    return UserActionHandler()

