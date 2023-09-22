from fastapi import APIRouter, Depends
from functools import lru_cache
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.db.database import async_engine, Base, get_async_session, redis_conn

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
async def redis_check():
    try:
        result = await redis_conn.ping()
        return {
            "status": "success",
            "data": result,
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "details": None
        }


@router.get("/postgresql")
async def db_check(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(1))
        return {
            "status": "success",
            "data": result.scalar(),
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "details": None
        }


@router.on_event("startup")
async def init_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


