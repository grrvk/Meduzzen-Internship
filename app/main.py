import sys
from fastapi import FastAPI
import uvicorn

sys.path.append(".")
from app.routers import router
from app.core.config import settings

app = FastAPI()

app.include_router(router.router)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.fast_api_host,
                port=settings.fast_api_port,
                reload=settings.fast_api_reload
                )
