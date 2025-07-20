from typing import Annotated

from starlette import status
from fastapi import Depends

from common.dependencies.authorization_dep import SessionID
from redis_client.utils import get_value_by_key
from users.models.users_db import Users


async def get_user_by_email(email: str) -> Users:
    user = await Users.find_first_by_kwargs(email=email)
    if user is None:
        raise status.HTTP_401_UNAUTHORIZED
    return user

GetUserByEmail = Annotated[Users, Depends(get_user_by_email)]


async def get_current_authorized_user(current_session_id: SessionID) -> Users:
    user_id = await get_value_by_key(key=current_session_id)
    return await Users.find_first_by_id(user_id)


GetCurrentAuthorizedUser = Annotated[Users, Depends(get_current_authorized_user)]
