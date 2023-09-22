from typing import AsyncGenerator

from redis import asyncio as aioredis
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import db_settings, redis_settings

DATABASE_URL = (f"postgresql+asyncpg://{db_settings.db_user}:{db_settings.db_pass}@{db_settings.db_host}:"
                f"{db_settings.db_port}/{db_settings.db_name}")

REDIS_URL = f"redis://{redis_settings.redis_host}:{redis_settings.redis_port}/0"

Base = declarative_base()

metadata = MetaData()

async_engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(async_engine)

redis_conn = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


