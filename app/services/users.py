from fastapi import HTTPException

from app.schemas.schema import UserSignUpRequest, UserUpdateRequest
from app.services.hasher import hasher
from app.utils.repository import AbstractRepository, SQLAlchemyRepository


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def add_user(self, user: UserSignUpRequest):
        if await self.users_repo.get_one_by(**dict(user_email=user.user_email)):
            raise HTTPException(status_code=400, detail="user with such email already exists")
        users_dict = user.model_dump()
        users_dict["hashed_password"] = hasher.get_password_hash(users_dict["hashed_password"])
        user_id = await self.users_repo.create_one(users_dict)
        return user_id

    async def get_all_users(self):
        users = await self.users_repo.get_all()
        return users

    async def get_user_by_email(self, user_email: str):
        user = await self.users_repo.get_one_by(**dict(user_email=user_email))
        if not user:
            raise HTTPException(status_code=400, detail="no user with such id")
        return user

    async def get_user_by_id(self, user_id: int):
        user = await self.users_repo.get_one_by(**dict(id=user_id))
        if not user:
            raise HTTPException(status_code=400, detail="no user with such id")
        return user

    async def edit_user(self, id: int, data: UserUpdateRequest):
        await self.get_user_by_id(id)
        users_dict = data.model_dump()
        user_id = await self.users_repo.update_one(id, users_dict)
        return user_id

    async def delete_user(self, id: int):
        await self.get_user_by_id(id)
        await self.users_repo.delete_one(id)
        return True
