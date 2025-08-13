from contextlib import asynccontextmanager
from pathlib import Path
from typing import Callable, Awaitable

import uvicorn
from fastapi import FastAPI
from requests import Response
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from common.config import sessionmaker
from common.sqlalchemy_ext import session_context
from redis_client.redis_controller import RedisController
from users.routes.auth_rest import auth_router
from users.routes.sessions_test import sessions_test_router
from users.routes.users_rest import user_router
from posts.routes.posts_rest import post_router


BASE_DIR = Path(__file__).parent


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    redis_controller = RedisController()
    fastapi_app.state.redis_controller = redis_controller
    yield
    await redis_controller.close()


app = FastAPI(title="Форум для фанатов Ворониных", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router)
app.include_router(sessions_test_router)


@app.middleware("http")
async def database_session_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    async with sessionmaker.begin() as session:
        session_context.set(session)
        return await call_next(request)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
