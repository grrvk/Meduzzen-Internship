import sys
from fastapi import FastAPI
import uvicorn

sys.path.append(".")
from app.routers import router
from app.core.config import settings
from app.db.database import async_engine, Base

app = FastAPI()

app.include_router(router.router)


@app.on_event("startup")
async def init_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.fast_api_host,
                port=settings.fast_api_port,
                reload=settings.fast_api_reload
                )
