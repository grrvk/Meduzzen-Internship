from redis import asyncio as aioredis
from fastapi import APIRouter, Depends
from functools import lru_cache
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings
from app.db.database import async_engine, get_async_session, REDIS_URL

router = APIRouter()

Session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


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


@router.on_event("startup")
async def startup_event():
    redis_conn = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
