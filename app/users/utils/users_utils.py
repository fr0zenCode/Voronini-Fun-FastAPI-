from starlette import status
from fastapi import Response, HTTPException

from common.dependencies.authorization_dep import SessionID
from redis_client.dependencies.redis_dep import GetRedisController
from users.aliases import INCORRECT_EMAIL_OR_PASSWORD_ALIAS, SESSION_KEY_IN_COOKIES, UNAUTHORIZED_ALIAS
from users.dependencies.auth_dep import GetAuthenticatedUserID
from users.models.users_db import Users
from users.utils.sessions_utils import generate_session_id, set_session_in_cookie
from users.utils.unique_checkers import is_email_unique, is_username_unique


async def create_user_util(user_data: Users.InputSchema) -> Users:
    dumped_user_data = user_data.model_dump()
    await is_email_unique(email=dumped_user_data["email"])
    await is_username_unique(username=dumped_user_data["username"])
    return await Users.create(**dumped_user_data)


async def login_util(
        response: Response,
        redis_controller: GetRedisController,
        user_id: GetAuthenticatedUserID
) -> None:
    if user_id:
        session_id = generate_session_id()
        await redis_controller.set(key=session_id, value=user_id)
        await set_session_in_cookie(response=response, session_id=session_id)
    else:
        # TODO: log
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INCORRECT_EMAIL_OR_PASSWORD_ALIAS)


async def logout_util(
        response: Response,
        redis_controller: GetRedisController,
        current_session_id: SessionID
):
    response.delete_cookie(key=SESSION_KEY_IN_COOKIES)
    try:
        await redis_controller.delete(key=current_session_id)
    except Exception as e:
        print(e) # TODO: log
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UNAUTHORIZED_ALIAS)
