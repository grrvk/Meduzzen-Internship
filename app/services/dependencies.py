from app.repositories.users import UsersRepository
from app.services.users import UsersService


def users_service():
    return UsersService(UsersRepository)