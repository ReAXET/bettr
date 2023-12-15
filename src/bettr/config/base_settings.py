import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Union

from dotenv import load_dotenv

load_dotenv()


class BaseSettings:
    """Base settings for Bettr application"""

    # ENV Config
    ENV: str = os.getenv('ENV', 'dev')

    # Database Config
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '5432'))
    DB_NAME: str = os.getenv('DB_NAME', 'sportsdb')
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'postgres')

    # Redis Config
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD', 'redis')

    # Celery Config
    CELERY_REDIS_HOST: str = os.getenv('CELERY_REDIS_HOST', 'localhost')
    CELERY_REDIS_PORT: int = int(os.getenv('CELERY_REDIS_PORT', '6379'))
    CELERY_REDIS_DB: int = int(os.getenv('CELERY_REDIS_DB', '0'))
    CELERY_REDIS_PASSWORD: str = os.getenv('CELERY_REDIS_PASSWORD', 'redis')
    CELERY_BROKER_URL: str = os.getenv(
        'CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_REDIS_DB: int = int(os.getenv('CELERY_BROKER_REDIS_DB', '0'))
    CELERY_BACKEND_REDIS_DB: int = int(
        os.getenv('CELERY_BACKEND_REDIS_DB', '0'))

    # RabbitMQ Config
    RABBITMQ_HOST: str = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT: int = int(os.getenv('RABBITMQ_PORT', '5672'))
    RABBITMQ_USER: str = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD: str = os.getenv('RABBITMQ_PASSWORD', 'guest')
    RABBITMQ_VHOST: str = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_BROKER_URL: str = os.getenv(
        'RABBITMQ_BROKER_URL', 'amqp://guest:guest@localhost:5672/')

    # Token Config
    JWT_SECRET: str = os.getenv('JWT_SECRET', 'my-secret-key')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', '240'))


class DevelopmentSettings(BaseSettings):
    """Settings for Bettr application in development environment"""

    # Override necessary values here
    pass


class ProductionSettings(BaseSettings):
    """Settings for Bettr application in production environment"""

    # Override necessary values here
    pass


@lru_cache
def get_settings(env: str = os.getenv('ENV', 'dev')) -> BaseSettings:
    if env == 'dev':
        return DevelopmentSettings()
    elif env == 'prod':
        return ProductionSettings()
    else:
        raise ValueError(f'Unknown environment: {env}')


settings = get_settings()


class Settings(BaseSettings):
    """Base settings for Bettr application"""

    # ENV Config
    ENV: Literal["dev", "prod"]

    # Database Config
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Redis Config
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str

    # Celery Config
    CELERY_REDIS_HOST: str
    CELERY_REDIS_PORT: int
    CELERY_REDIS_DB: int
    CELERY_REDIS_PASSWORD: str
    CELERY_BROKER_URL: str
    CELERY_BROKER_REDIS_DB: int
    CELERY_BACKEND_REDIS_DB: int

    # RabbitMQ Config
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str
    RABBITMQ_BROKER_URL: str

    # Token Config
    TOKEN_SECRET_KEY: str  # secrets.token.urlsafe(32)

    # Opera Log Config
    OPERA_LOG_ENCRYPT_SECRET_KEY: str

    # FastAPI Config
    API_V1_STR: str = '/api/v1'
    TITLE: str = 'Bettr Bettor'
    VERSION: str = '0.1.0'
    DESCRIPTION: str = 'Bettr Bettor API'
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOC_URL: str | None = f'{API_V1_STR}/redoc'
    OPENAPI_URL: str | None = f'{API_V1_STR}/openapi.json'
    DEBUG: bool = False
    LOG_LEVEL: str = 'info'

    def validate_openapi_url(cls, values) -> Any:
        if values['ENV'] == 'prod':
            values['OPENAPI_URL'] = None
        return values

    # Demo Mode Config
    DEMO_MODE: bool = False
    # If True then only GET, and OPTIONS requests are allowed
    # for all endpoints.
    DEMO_MODE_EXCLUDE: set[tuple[str, str]] = {
        ('POST', f'{API_V1_STR}/auth/login'),
        ('POST', f'{API_V1_STR}/auth/logout'),
        ('POST', f'{API_V1_STR}/auth/register'),
        ('POST', f'{API_V1_STR}/auth/refresh'),
        ('POST', f'{API_V1_STR}/auth/verify'),
        ('POST', f'{API_V1_STR}/auth/password-reset'),
        ('POST', f'{API_V1_STR}/auth/password-reset/confirm'),
        ('GET', f'{API_V1_STR}/auth/captcha')
    }
    UVICORN_HOST: str = 'localhost'
    UVICORN_PORT: int = 8000
    UVICORN_RELOAD: bool = True
    UVICORN_ACCESS_LOG: bool = True
    UVICORN_ACCESS_LOG_FORMAT: str = '%(asctime)s - %(levelname)s - %(message)s'
    UVICORN_LOG_LEVEL: str = 'info'

    # Static Server
    STATIC_FILES: bool = False

    # Location Parsing
    LOCATION_PARSE: Literal['online', 'offline', 'false'] = 'offline'

    # Limiter
    LIMITER_REDIS_PREFIX: str = 'bettr_limiter'

    # DateTime Config
    DATETIME_TZ: str = 'Central'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S %Z%z'
    DATETIME_FORMAT_NO_TZ: str = '%Y-%m-%d %H:%M:%S'

    # PGSQL Config
    PGSQL_ECHO: bool = False
    PGSQL_DATABASE: str = 'fba-bettr'
    PGSQL_HOST: str = 'localhost'
    PGSQL_CHARSET: str = 'utf8mb4'

    # Redis Config
    REDIS_TIMEOUT: int = 5

    # Token Configs
    TOKEN_ALGORITHM: str = 'HS256'
    TOKEN_EXPIRATION: int = 60 * 60 * 24 * 1
    TOKEN_REFRESH_EXPIRATION: int = 60 * 60 * 24 * 7
    TOKEN_URL_SWAGGER: str = f'{API_V1_STR}/auth/swagger_login'
    TOKEN_REDIS_PREFIX: str = 'bettr_token'
    TOKEN_REFRESH_REDIS_PREFIX: str = 'bettr_refresh_token'
    TOKEN_EXCLUDE: list[str] = [
        f'{API_V1_STR}/auth/login',
        f'{API_V1_STR}/auth/logout',
        f'{API_V1_STR}/auth/register',
        f'{API_V1_STR}/auth/refresh',
        f'{API_V1_STR}/auth/verify',
        f'{API_V1_STR}/auth/password-reset',
        f'{API_V1_STR}/auth/password-reset/confirm',
        f'{API_V1_STR}/auth/captcha'

    ]

    # Captcha
    CAPTCHA_REDIS_PREFIX: str = 'bettr_captcha'
    CAPTCHA_EXPIRATION: int = 60 * 60 * 24 * 1

    # Log Config
    LOG_STDOUT_FILENAME: str = 'bettr_access.log'
    LOG_STDERR_FILENAME: str = 'bettr_error.log'

    # Middleware Config
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_CORS_ALLOW_ORIGINS: list[str] = ['*']
    MIDDLEWARE_CORS_ALLOW_CREDENTIALS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = False

    # Casbin
    CASBIN_MODEL_PATH: str = 'casbin/model.conf'
    CASBIN_EXCLUDE: set[tuple[str, str]] = {
        ('POST', f'{API_V1_STR}/auth/swagger_login'),
        ('POST', f'{API_V1_STR}/auth/login'),
        ('POST', f'{API_V1_STR}/auth/logout'),
        ('POST', f'{API_V1_STR}/auth/register'),
        ('GET', f'{API_V1_STR}/auth/captcha')
    }

    # Menus
    MENU_PERMMISSION: bool = False
    MENU_EXCLUDE: list[str] = [
        'auth:swagger_login:post',
        'auth:login:post',
        'auth:logout:post',
        'auth:register:post',
        'auth:captcha:get'
    ]

    # OPERA Log
    OPERA_LOG_EXCLUDE: list[str] = [
        '/favicon.ico',
        DOCS_URL,
        REDOC_URL,
        OPENAPI_URL,
        f'{API_V1_STR}/auth/swagger_login',

    ]
    OPERA_LOG_ENCRYPT: int = 1  # 0: AES; 1: MD5; 2: ItsDangerous; 3: others;
    OPERA_LOG_ENCRYPT_INCLUDE: list[str] = [
        'password', 'old_password', 'new_password', 'confirm_password']

    # Ip Config
    IP_LOCATION_REDIS_PREFIX: str = 'bettr_ip_locate'
    IP_LOCATION_EXPIRATION: int = 60 * 60 * 24 * 1

    # Celery
    CELERY_BROKER: Literal['rabbitmq', 'redis'] = 'redis'
    CELERY_BACKEND_REDIS_PREFIX: str = 'bettr_celery'
    CELERY_BACKEND_REDIS_TIMEOUT: float = 5.0
    CELERY_BACKEND_REDIS_ORDERED: bool = True
    CELERY_BEAT_SCHEDULE_FILE: str = './log/celery-beat-schedule'
    CELERY_BEAT_SCHEDULE: dict[str, Any] = {
        'test': {
            'task': 'bettr.tasks.test',
            'schedule': 60.0,
            'args': ('test', )
        }
    }

    def validate_celery_broker(cls, values):
        if values['ENV'] == 'prod':
            values['CELERY_BROKER'] = 'rabbitmq'
        return values


#    class Config:
#        env_file = '.env'
#        env_file_encoding = 'utf-8'
#        case_sensitive = True
#        extra = 'ignore'
#        use_enum_values = True
#        validate_assignment = True
#        arbitrary_types_allowed = True
#        json_encoders = {
#            'datetime': lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S'),
#            'date': lambda d: d.strftime('%Y-%m-%d'),
#            'time': lambda t: t.strftime('%H:%M:%S')
#        }
