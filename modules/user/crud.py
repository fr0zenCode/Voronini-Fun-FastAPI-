import uuid
from typing import Callable

from pydantic import EmailStr
from sqlalchemy import text

from db.database import async_session_factory
from db.models import Users
from modules.user.schemas import UserRepresentation


class UserCRUD:

    def __init__(self, session_factory: Callable):
        self._session_factory = session_factory

    async def add_user_to_db(
            self,
            first_name: str,
            second_name: str,
            username: str,
            email: EmailStr,
            password: bytes,
            is_active: bool = True
    ) -> dict:
        user = Users(
            user_id=str(uuid.uuid4()),
            first_name=first_name,
            second_name=second_name,
            username=username,
            email=email,
            password=password,
            is_active=is_active
        )
        async with self._session_factory() as session:
            session.add(user)
            await session.commit()
        return {"message": "successful"}

    def change_first_name(self):
        ...

    def change_second_name(self):
        ...

    def change_username(self):
        ...

    def change_password(self):
        ...

    async def __select_users_from_db(self, where_params: str, values: dict) -> UserRepresentation:
        async with self._session_factory() as session:
            stmt = text(f"""SELECT * FROM users WHERE {where_params};""")
            result = await session.execute(stmt, values)
            obj = result.first()
            return UserRepresentation(
                user_id=obj[0],
                first_name=obj[1],
                second_name=obj[2],
                username=obj[3],
                email=obj[4],
                password=obj[5]
            )

    async def delete_user_by_id(self, user_id: str) -> dict:
        async with self._session_factory() as session:
            stmt = text("""DELETE FROM users WHERE users.user_id=:user_id;""")

            session.execute(stmt, {"user_id": user_id})
            session.commit()
            return {"message": "successful"}

    async def verify_user_by_email_and_password(self, email: EmailStr, password: str) -> bool:
        ...

    async def get_user_by_email(self, email: EmailStr) -> UserRepresentation:
        return await self.__select_users_from_db(
            where_params="users.email=:email",
            values={"email": email}
        )

    async def get_user_by_username(self, username: str) -> UserRepresentation:
        return await self.__select_users_from_db(
            where_params="users.username=:username",
            values={"username": username}
        )

    async def get_user_by_id(self, user_id: str) -> UserRepresentation:
        return await self.__select_users_from_db(
            where_params="users.user_id=:user_id",
            values={"user_id": user_id}
        )

    async def deactivate_user(self, email: EmailStr, password: str):
        ...


user_crud = UserCRUD(async_session_factory)
