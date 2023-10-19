import sys
from fastapi import FastAPI
import uvicorn
from fastapi.security import OAuth2PasswordBearer

from app.models.model import Base
from app.routers.notifications import scheduler

sys.path.append(".")
from app.routers import (router, companies, auth_router, users, actions, quizzes, results, answers, analytics,
                         notifications)
from app.core.config import settings
from app.db.database import async_engine

app = FastAPI()

app.include_router(router.router)
app.include_router(users.router)
app.include_router(auth_router.router)
app.include_router(companies.router)
app.include_router(actions.router)
app.include_router(quizzes.router)
app.include_router(results.router)
app.include_router(answers.router)
app.include_router(analytics.router)
app.include_router(notifications.router)


@app.on_event("startup")
async def start_scheduler():
    scheduler.start()


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.fast_api_host,
                port=settings.fast_api_port,
                reload=settings.fast_api_reload
                )
