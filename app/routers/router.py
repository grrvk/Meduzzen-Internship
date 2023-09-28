from redis import Redis
from fastapi import APIRouter, Depends, Response
from functools import lru_cache
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.db.database import get_async_session, get_redis_db
from app.repositories.users import UsersRepository
from app.schemas.schema import UserSchema, UserSignUpRequest, UserUpdateRequest
from app.services.dependencies import users_service
from app.services.users import UsersService

router = APIRouter()


@router.get("/")
def health_check():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


@lru_cache()
def get_settings():
    return Settings()


@router.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "host": settings.fast_api_host,
        "port": settings.fast_api_port,
    }


@router.get("/redis")
async def redis_check(db: Redis = Depends(get_redis_db)):
    try:
        result = await db.ping()
        return {
            "status": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        return {
            "status": 500,
            "error_message": str(e),
            "details": None
        }


@router.post("/add_user")
async def add_user(
        user: UserSignUpRequest,
        user_service: Annotated[UsersService, Depends(users_service)]
):
    user_id = await user_service.add_user(user)
    return {
            "status": 200,
            "data": user_id,
            "details": None
        }


@router.put("/users/{user_id}")
async def add_user(
        user_id: int,
        user: UserUpdateRequest,
        user_service: Annotated[UsersService, Depends(users_service)]
):
    user_id = await user_service.edit_user(user_id, user)
    return {
        "status": 200,
        "data": user_id,
        "details": None
    }


@router.delete("/users/{user_id}")
async def add_user(
        user_id: int,
        user_service: Annotated[UsersService, Depends(users_service)]
):
    res = await user_service.delete_user(user_id)
    return {
        "status": 200,
        "data": res,
        "details": "deleted"
    }


@router.get("/users")
async def get_all_users(
        user_service: Annotated[UsersService, Depends(users_service)]
):
    users = await user_service.get_all_users()
    return users


@router.get("/users/{user_id}")
async def read_item(
        user_id: int,
        user_service: Annotated[UsersService, Depends(users_service)]
):
    user = await user_service.get_user_by_id(user_id)
    return user


@router.get("/postgresql")
async def db_check(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(1))
        return {
            "status": 200,
            "data": result.scalar(),
            "details": None
        }
    except Exception as e:
        return {
            "status": 500,
            "error_message": str(e),
            "details": None
        }
