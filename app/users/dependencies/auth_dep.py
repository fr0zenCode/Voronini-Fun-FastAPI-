from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

from users.dependencies.users_dep import GetUserByEmail


class InputPasswordSchema(BaseModel):
    password: str


async def is_user_authenticate_successfully(
        user: GetUserByEmail,
        password_schema: InputPasswordSchema
) -> int | bool:
    if user.is_password_valid(password=password_schema.password):
        return user.id
    return False

GetAuthenticatedUserID = Annotated[int | bool, Depends(is_user_authenticate_successfully)]
