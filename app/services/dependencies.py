from app.repositories.users import UsersRepository

from .users import UserService


def users_service():
    return UserService(UsersRepository)