from redis import Redis
from fastapi import APIRouter, Depends
from functools import lru_cache
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.db.database import get_async_session, get_redis_db


router = APIRouter(tags=["default"])


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
