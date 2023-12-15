import datetime
import logging
import time
from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, List, Literal, Optional, Tuple, Union, cast
from pydantic import BaseModel, Extra, Field, HttpUrl, root_validator, validator
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import ORJSONResponse
from fastapi.middleware.wsgi import WSGIMiddleware
from itsdangerous import URLSafeTimedSerializer
from loguru import logger
from celery import Celery
from redis import Redis
from itsdangerous import URLSafeTimedSerializer


class AppConfig(BaseModel):
    ...


config = AppConfig()


class User(BaseModel):
    username: str
    password: str
    # ...


def encrypt_password(password: str) -> str:
    # Implement password encryption
    return password


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = User(username=username, password=password)
    return user


def get_user(username: str) -> Optional[User]:
    user = User(username=username, password='')
    return user


def get_password_hash(password: str) -> str:
    return password


def verify_password(password: str, hashed_password: str) -> bool:
    return password == hashed_password


class Dependency(object):
    def __init__(self, request: Request) -> None:
        self.request = request

    async def authenticate(self) -> User:
        if 'username' not in self.request.session:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        username = self.request.session['username']
        password = self.request.session['password']
        user = authenticate_user(username, password)
        if user is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return user

    async def login(self, username: str, password: str) -> User:
        user = get_user(username)
        if user is None:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        self.request.session['username'] = username
        self.request.session['password'] = password
        return user

    async def logout(self) -> None:
        if 'username' in self.request.session:
            del self.request.session['username']
        if 'password' in self.request.session:
            del self.request.session['password']


app = FastAPI()

# Loguru setup
logger.remove()
logger.add("log/bettr.log", level=logging.INFO,
           format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level} {message}")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(Dependency(Request).authenticate)):
    return current_user


@app.post("/users/login")
async def login_for_access_token(request: Request, form_data: User):
    user = await Dependency(request).login(form_data.username, form_data.password)
    return {"username": user.username}


@app.post("/users/logout")
async def logout_for_access_token(request: Request):
    await Dependency(request).logout()
    return {"message": "logout success"}


# Celery setup
celery = Celery("tasks", broker=config.CELERY_BROKER_URL)


@celery.task
def add(x: int, y: int) -> int:
    return x + y


@app.get("/tasks/add")
async def add_task(x: int, y: int):
    result = await asyncio.get_event_loop().run_in_executor(None, add, x, y)
    return {"result": result}


# Redis setup
redis = Redis.from_url(config.REDIS_URL)
serializer = URLSafeTimedSerializer(config.SECRET_KEY)


@app.get("/tasks/cache/{item}")
async def cache_item(item: str):
    result = redis.get(item)
    if result is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Item not found in cache")
    return {"item": item, "value": result.decode()}


@app.put("/tasks/cache/{item}")
async def set_item(item: str, value: str):
    redis.set(item, value)
    return {"item": item, "value": value}


@app.delete("/tasks/cache/{item}")
async def delete_item(item: str):
    result = redis.delete(item)
    if result == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Item not found in cache")
    return {"item": item}


# Finalize and run the application
app.include_router(api.router)
