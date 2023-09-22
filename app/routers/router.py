from redis import asyncio as aioredis
from fastapi import APIRouter, Depends
from functools import lru_cache
from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.db.database import async_engine, REDIS_URL, Base, SessionLocal, get_async_session

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
    redis_conn = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    result = await redis_conn.ping()
    return {
        "redis-health": result,
    }


@router.get("/postgresql")
async def db_check(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(1)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.scalar(),
            "details": None
        }
    except Exception:
        return {
            "status": "error",
            "data": None,
            "details": None
        }


@router.on_event("startup")
async def startup_event():
    redis_conn = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)


@router.on_event("startup")
async def init_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


