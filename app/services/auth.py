import secrets
from datetime import datetime, timezone

from fastapi import HTTPException
from app.auth.jwt import verify_password, get_password_hash, create_access_token
from app.schemas.schema import UserSignUpRequest, Token
from app.utils.repository import AbstractRepository


class AuthService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def authenticate_user(self, email, password):
        user_db = await self.users_repo.get_one_by(user_email=email)
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

        access_token = create_access_token(
            data={"sub": user_db.user_email}
        )

        return Token(access_token=access_token, token_type="Bearer")

    async def get_user_by_payload(self, payload: dict):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if payload is None:
            raise credentials_exception

        scope = payload.get("scope")
        if scope == "openid profile email":
            email = payload.get("user_email")
            user = await self.users_repo.get_one_by(user_email=email)
            if user is None:
                added_user = UserSignUpRequest(user_email=email, hashed_password=secrets.token_urlsafe(15),
                                               user_firstname="string", user_lastname="string",
                                               created_at=datetime.now(timezone.utc)
                                               )
                user_dict = added_user.model_dump()
                user_dict["hashed_password"] = get_password_hash(user_dict["hashed_password"].lower())
                user_id = await self.users_repo.create_one(user_dict)
                return await self.users_repo.get_one_by(id=user_id)
            return user
        if scope == "secret jwt":
            email = payload.get("sub")
            user = await self.users_repo.get_one_by(user_email=email)
            if user is None:
                raise credentials_exception
            return user
