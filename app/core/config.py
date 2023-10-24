from dotenv import load_dotenv
from pydantic_settings import BaseSettings

import os

load_dotenv()


class Settings(BaseSettings):
    fast_api_host: str = str(os.getenv("SERVER_HOST"))
    fast_api_port: int = os.getenv("SERVER_PORT")
    fast_api_reload: bool = os.getenv("SERVER_RELOAD")


settings = Settings()


class DbSettings(BaseSettings):
    db_host: str = str(os.environ.get("DB_HOST"))
    db_port: int = os.environ.get("DB_PORT")
    db_name: str = os.environ.get("DB_DATABASE")
    db_user: str = os.environ.get("DB_USERNAME")
    db_pass: str = os.environ.get("DB_PASSWORD")


db_settings = DbSettings()


class RedisSettings(BaseSettings):
    redis_host: str = os.environ.get("REDIS_HOST")
    redis_port: int = os.environ.get("REDIS_PORT")
    expire_time: int = os.environ.get("REDIS_EXPIRE_TIME")

redis_settings = RedisSettings()


class Auth0Settings(BaseSettings):
    domain: str = os.environ.get("DOMAIN")
    api_audience: str = os.environ.get("API_AUDIENCE")
    issuer: str = os.environ.get("ISSUER")


auth0_settings = Auth0Settings()
