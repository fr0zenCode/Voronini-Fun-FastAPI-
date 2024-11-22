import uuid
from typing import Callable

from pydantic import EmailStr
from sqlalchemy import text, select

from db.database import async_session_factory
from db.models import Tokens
from modules.user.schemas import UserRepresentation


class TokensCRUD:

    def __init__(self, session_factory: Callable = async_session_factory()):
        self._session_factory = session_factory

    async def add_refresh_jwt_token_to_db(self, user_id: str, refresh_jwt_token: str) -> dict:

        refresh_token = Tokens(user_id=user_id, refresh_token=refresh_jwt_token)

        async with self._session_factory() as session:
            session.add(refresh_token)
            await session.commit()

        return {"message": "successful"}

    async def __select_token_from_db(self, where_params: str, values: dict):
        async with self._session_factory() as session:
            stmt = text(f"""SELECT * FROM tokens WHERE {where_params};""")
            result = await session.execute(stmt, values)
            obj = result.first()
            return {"user_id": obj[1], "refresh_token": obj[0]}

    async def is_refresh_token_exists(self, user_id):
        try:
            result = await self.__select_token_from_db(where_params="tokens.user_id=:user_id", values={"user_id": user_id})
            if result:
                return True
        except Exception:
            print('ERROR ::::: auth/crud.py/is_refresh_token_exists')
            return False

    async def get_refresh_token_by_user_id(self, user_id):
        result = await self.__select_token_from_db(
            where_params="tokens.user_id=:user_id",
            values={"user_id": user_id}
        )
        return result

    async def delete_token_by_user_id(self, user_id: str):
        async with self._session_factory() as session:
            stmt = text(f"""DELETE FROM tokens WHERE tokens.user_id = :user_id;""")
            await session.execute(stmt, {"user_id": user_id})
            await session.commit()


tokens_crud = TokensCRUD(async_session_factory)
