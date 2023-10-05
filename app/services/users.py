from fastapi import HTTPException

from app.schemas.schema import UserSignUpRequest, UserUpdateRequest, UserSignInRequest
from app.utils.repository import AbstractRepository
from app.auth.jwt import get_password_hash, verify_password


class UserService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def add_user(self, user: UserSignUpRequest):
        if await self.users_repo.get_one_by(user_email=user.user_email):
            raise HTTPException(status_code=400, detail="user with such email already exists")
        users_dict = user.model_dump()
        hashed = get_password_hash(users_dict["hashed_password"].lower())
        users_dict["hashed_password"] = hashed
        user_id = await self.users_repo.create_one(users_dict)
        return user_id


    async def authenticate_user(self, email, password):
        user_db = await self.users_repo.get_one_by(**dict(user_email=email))
        if user_db is None:
            raise HTTPException(
                status_code=400,
                detail="Incorrect email or password"
            )
        if not verify_password(password.lower(), user_db.hashed_password):
            raise HTTPException(
                status_code=400,
                detail="Incorrect email or password"
            )
        return user_db

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

    async def edit_user(self, id: int, data: UserUpdateRequest):
        await self.get_user_by_id(id)
        users_dict = data.model_dump()
        user_id = await self.users_repo.update_one(id, users_dict)
        return user_id

    async def delete_user(self, id: int):
        await self.get_user_by_id(id)
        await self.users_repo.delete_one(id)
        return True
