from starlette import status
from fastapi import APIRouter, Response

from common.dependencies.authorization_dep import SessionID
from redis_client.dependencies.redis_dep import GetRedisController
from users.dependencies.auth_dep import GetAuthenticatedUserID
from users.utils.users_utils import login_util, logout_util

auth_router = APIRouter(prefix="/users", tags=["auth"])


@auth_router.post(path="/auth/login/", status_code=status.HTTP_200_OK, summary="Login")
async def login(
        response: Response,
        redis_controller: GetRedisController,
        user_id: GetAuthenticatedUserID
) -> None:
    await login_util(response, redis_controller, user_id)


@auth_router.post(path="/auth/logout/", status_code=status.HTTP_204_NO_CONTENT, summary="Logout")
async def logout(
        response: Response,
        redis_controller: GetRedisController,
        current_session_id: SessionID
) -> None:
    await logout_util(response, redis_controller, current_session_id)
