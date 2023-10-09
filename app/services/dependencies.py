from app.repositories.users import UsersRepository
from .auth import AuthService
from .permissions import UserPermissions
from .users import UsersService
from app.repositories.auth import AuthRepository


def users_service():
    return UsersService(UsersRepository)


def authentication_service():
    return AuthService(AuthRepository)


def permissions_service():
    return UserPermissions()