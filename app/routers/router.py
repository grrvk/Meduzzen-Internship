from redis import asyncio as aioredis
from fastapi import APIRouter, Depends
from functools import lru_cache
from typing import Annotated

from app.core.config import Settings
from app.db.database import async_engine, REDIS_URL

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
async def get_specific_operations():
    try:
        async with async_engine.connect() as connection:
            await connection.begin()
            return {"postgres_status": "ok"}
    except Exception as e:
        return {"postgres_status": "error", "error_message": str(e)}


@router.on_event("startup")
async def startup_event():
    redis_conn = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
