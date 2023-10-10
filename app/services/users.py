from fastapi import HTTPException

from app.models.model import User
from app.schemas.schema import UserSignUpRequest, UserUpdateRequest, UserSignInRequest
from app.services.permissions import UserPermissions
from app.utils.repository import AbstractRepository
from app.auth.jwt import get_password_hash, verify_password


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()
        self.permission_service = UserPermissions()

    async def add_user(self, user: UserSignUpRequest, current_user: User):
        await self.permission_service.can_add_user(current_user)
        if await self.users_repo.get_one_by(user_email=user.user_email):
            raise HTTPException(status_code=400, detail="user with such email already exists")
        users_dict = user.model_dump(exclude_unset=True)
        hashed = get_password_hash(users_dict["hashed_password"].lower())
        users_dict["hashed_password"] = hashed
        user_id = await self.users_repo.create_one(users_dict)
        return user_id

    async def get_all_users(self):
        users = await self.users_repo.get_all()
        return users

    async def get_user_by_email(self, user_email: str):
        user = await self.users_repo.get_one_by(user_email=user_email)
        if not user:
            raise HTTPException(status_code=400, detail="no user with such email")
        return user

    async def get_user_by_id(self, user_id: int):
        user = await self.users_repo.get_one_by(id=user_id)
        if not user:
            raise HTTPException(status_code=400, detail="no user with such id")
        return user

    async def edit_user(self, id: int, data: UserUpdateRequest, current_user: User):
        users_dict = data.model_dump(exclude_unset=True)
        await self.permission_service.can_update_user(id, current_user, users_dict)
        if users_dict.get("hashed_password"):
            hashed = get_password_hash(users_dict["hashed_password"].lower())
            users_dict["hashed_password"] = hashed
        user_id = await self.users_repo.update_one(id, users_dict)
        return user_id

    async def delete_user(self, id: int, current_user: User):
        await self.permission_service.can_delete_user(id, current_user)
        await self.users_repo.delete_one(id)
        return True
