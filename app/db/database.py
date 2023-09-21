from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import db_settings, redis_settings

DATABASE_URL = (f"postgresql+asyncpg://{db_settings.db_user}:{db_settings.db_pass}@{db_settings.db_host}:"
                f"{db_settings.db_port}/{db_settings.db_name}")

REDIS_URL = f"redis://{redis_settings.redis_host}:{redis_settings.redis_port}"

async_engine = create_async_engine(DATABASE_URL)

Base = declarative_base()


async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session


