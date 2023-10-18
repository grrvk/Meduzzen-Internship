import sys
from fastapi import FastAPI
import uvicorn
from fastapi.security import OAuth2PasswordBearer

from app.models.model import Base

sys.path.append(".")
from app.routers import router, companies, auth_router, users, actions, quizzes
from app.core.config import settings
from app.db.database import async_engine

app = FastAPI()

app.include_router(router.router)
app.include_router(users.router)
app.include_router(auth_router.router)
app.include_router(companies.router)
app.include_router(actions.router)
app.include_router(quizzes.router)


#@app.on_event("startup")
#async def init_tables():
#    async with async_engine.begin() as conn:
#        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.fast_api_host,
                port=settings.fast_api_port,
                reload=settings.fast_api_reload
                )
