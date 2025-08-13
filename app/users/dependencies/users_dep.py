from typing import Annotated

from starlette import status
from fastapi import Depends, HTTPException

from common.dependencies.authorization_dep import SessionID
from redis_client.dependencies.redis_dep import GetRedisController
from users.aliases import INCORRECT_EMAIL_OR_PASSWORD_ALIAS, UNAUTHORIZED_ALIAS
from users.models.users_db import Users


async def get_user_by_email(email_schema: Users.EmailSchema) -> Users:
    user = await Users.find_first_by_kwargs(email=email_schema.email)
    if not user:
        # TODO: log
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=INCORRECT_EMAIL_OR_PASSWORD_ALIAS)
    return user

GetUserByEmail = Annotated[Users, Depends(get_user_by_email)]


async def get_current_authorized_user(
        redis_controller: GetRedisController,
        current_session_id: SessionID
) -> Users:
    try:
        user_id = await redis_controller.get(key=current_session_id)
        if not user_id:
            # TODO: log
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UNAUTHORIZED_ALIAS)
    except Exception as e:
        # TODO: log
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=UNAUTHORIZED_ALIAS)
    return await Users.find_first_by_id(user_id)

GetCurrentAuthorizedUser = Annotated[Users, Depends(get_current_authorized_user)]
