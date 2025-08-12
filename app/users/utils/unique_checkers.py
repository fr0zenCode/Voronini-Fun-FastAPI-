from fastapi import HTTPException

from ..models.users_db import Users


async def is_username_unique(username: str) -> None:
    if await Users.find_first_by_kwargs(username=username):
        raise HTTPException(status_code=400, detail="Пользователь с таким USERNAME уже существует") # todo: вынести в алиас

async def is_email_unique(email: str) -> None:
    if await Users.find_first_by_kwargs(email=email):
        raise HTTPException(status_code=400, detail="Пользователь с таким EMAIL уже существует") # todo: вынести в алиас
