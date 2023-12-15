"""Settings Class for the project."""

import os
from functools import lru_cache
from typing import Any, List, Literal, Union

from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv

from bettr.utilities.env_setup import Env


# Load the .env file
load_dotenv()


class Settings(BaseSettings):
    """Settings Class for the project."""
    model_config = SettingsConfigDict(extra='allow',
                                      env_file='.env', env_file_encoding='utf-8')

    # Directories
    ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SRC_DIR: str = os.path.join(ROOT_DIR, "src")
    DATA_DIR: str = os.path.join(ROOT_DIR, "data")
    CONFIG_DIR: str = os.path.join(ROOT_DIR, "config")
    DB_DIR: str = os.path.join(ROOT_DIR, "db")
    LOGS_DIR: str = os.path.join(ROOT_DIR, "logs")

    # Environmen
    TESTING: bool = False
    DEBUG: bool = False
    LOG_LEVEL: str = 'INFO'
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'
    LOG_FILE: str = os.path.join(LOGS_DIR, 'bettr.log')

    # Postgres DB
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'postgres')
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'postgres')
    POSTGRES_DB_URL_ASYNC: str = f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:{os.getenv(
        "POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    POSTGRES_DB_URL_SYNC: Any = f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv(
        "POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'
    POSTGRES_DB_POOL_SIZE: int = 10
    POSTGRES_DB_MAX_OVERFLOW: int = 10
    POSTGRES_DB_POOL_PRE_PING: bool = True

    # Supabase
    SUPABASE_DB_PASSWORD: str = os.getenv('SUPABASE_DB_PASSWORD', 'postgres')
    SUPABASE_ANON_PUBLIC: str = os.getenv('SUPABASE_ANON_PUBLIC', 'postgres')
    SUPABASE_ANON_SECRET: str = os.getenv('SUPABASE_ANON_SECRET', 'postgres')
    SUPABASE_JWT_KEY: str = os.getenv('SUPABASE_JWT_KEY', 'postgres')
    SUPABASE_PROJECT_URL: str = os.getenv('SUPABASE_PROJECT_URL', 'postgres')

    # Uvicorn
    UVICORN_HOST: str = '0.0.0.0'
    UVICORN_PORT: int = 8000
    UVICORN_RELOAD: bool = True

    # Redis
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: Union[str, int] = os.getenv('REDIS_PORT', 6379)
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD', '')
    REDIS_DB: Union[str, int] = os.getenv('REDIS_DB', 0)
    LIMITER_REDIS_PREFIX: str = 'bettr'
    LIMITER_ENABLED: bool = True
    REDIS_TIMEOUT: int = 5
    LOG_TRACES: bool = True

    # Datetime
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"
    TIME_FORMAT: str = "%H:%M:%S"
    DATETIME_TIMEZONE: str = 'America/Chicago'

    # FastAPI
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "bettr"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "bettr is a sports analytics platform for use with the over/under pick em's that have recently become popular."
    OPENAPI_URL: str | None = f"{API_V1_STR}/openapi"
    DOCS_URL: str | None = f"{API_V1_STR}/docs"
    REDOC_URL: str | None = f"{API_V1_STR}/redoc"

    # JWT
    # secrets.token_urlsafe(32) # Set up a custom secret key generator
    TOKEN_SECRET_KEY: str = os.getenv('TOKEN_SECRET_KEY', 'secret_key')
    TOKEN_ALGORITHM: Literal["HS256"] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    TOKEN_URL_SWAGGER: str = f'{API_V1_STR}/auth/swagger_login'
    TOKEN_REDIS_PREFIX: str = 'bettr'
    TOKEN_REDIS_REFRESH_PREFIX: str = 'bettr_refresh_token'
    TOKEN_EXCLUDE: List[str] = [
        f'{API_V1_STR}/auth/login',
    ]

    # Logging
    LOG_STDOUT_FILE: str = os.path.join(LOGS_DIR, 'bettr_stdout.log')
    LOG_STDERR_FILE: str = os.path.join(LOGS_DIR, 'bettr_stderr.log')
    LOG_STDOUT_LEVEL: str = 'INFO'
    LOG_STDERR_LEVEL: str = 'ERROR'
    LOG_STDOUT_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_STDERR_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_STDOUT_DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'
    LOG_STDERR_DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'


@lru_cache()
def get_settings() -> Settings:
    """Get the settings.

    Returns:
        Settings: The settings class.
    """
    return Settings()


settings = get_settings()
