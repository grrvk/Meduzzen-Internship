from app.repositories.users import UsersRepository
from .auth import AuthService
from .companies import CompaniesService
from .permissions import UserPermissions
from .users import UsersService
from app.repositories.auth import AuthRepository
from ..repositories.companies import CompaniesRepository


def users_service():
    return UsersService(UsersRepository)


def authentication_service():
    return AuthService(AuthRepository)


def companies_service():
    return CompaniesService(CompaniesRepository)


def permissions_service():
    return UserPermissions()
