from dotenv import load_dotenv
from pydantic_settings import BaseSettings

import os

load_dotenv()


class Settings(BaseSettings):
    fast_api_host: str = str(os.getenv("SERVER_HOST"))
    fast_api_port: int = os.getenv("SERVER_PORT")
    fast_api_reload: bool = os.getenv("SERVER_RELOAD")


settings = Settings()
