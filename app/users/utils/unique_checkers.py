from fastapi import HTTPException

from users.aliases import EMAIL_ALREADY_TAKEN_ALIAS, USERNAME_ALREADY_TAKEN_ALIAS
from users.models.users_db import Users


async def is_username_unique(username: str) -> None:
    if await Users.find_first_by_kwargs(username=username):
        raise HTTPException(status_code=400, detail=USERNAME_ALREADY_TAKEN_ALIAS)

async def is_email_unique(email: str) -> None:
    if await Users.find_first_by_kwargs(email=email):
        raise HTTPException(status_code=400, detail=EMAIL_ALREADY_TAKEN_ALIAS)
