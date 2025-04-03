import datetime
from dataclasses import dataclass

from pydantic import EmailStr
from sqlalchemy import insert, update, select

from database.core.database import async_session_factory
from database.core.models import Users
from database.repositories.users.repository.abstract import AbstractUsersRepository
from database.repositories.users.schemas import UserAddSchema, UserSchema


@dataclass
class SQLAlchemyUsersRepository(AbstractUsersRepository):

    _async_session_factory = async_session_factory

    async def add_user(self, user: UserAddSchema) -> int:
        async with self._async_session_factory() as session:
            stmt = insert(Users).values(
                first_name=user.first_name,
                second_name=user.second_name,
                username=user.username,
                email=user.email,
                password=user.password,
                is_active=True
            ).returning(Users.id)
            added_user_id = await session.execute(stmt)
            await session.commit()
            return added_user_id.scalar_one()

    async def delete_user_by_id(self, user_id: int) -> dict:
        async with self._async_session_factory() as session:
            stmt = update(Users).where(Users.id == user_id).values(is_active=False)
            await session.execute(stmt)
            await session.commit()
            return {
                "message": "successful",
                "detail": f"user with id {user_id} deleted"
            }

    async def get_user_by_id(self, user_id: int) -> UserSchema:
        async with self._async_session_factory() as session:
            stmt = select(Users).where(Users.id == user_id)
            user = await session.execute(stmt)
            return user.scalar_one().convert_to_pydantic_model()

    async def get_user_by_email(self, email: EmailStr) -> UserSchema:
        async with self._async_session_factory() as session:
            stmt = select(Users).where(Users.email == email)
            user = await session.execute(stmt)
            return user.scalar_one().convert_to_pydantic_model()

    async def get_user_by_username(self, username: str) -> UserSchema:
        async with self._async_session_factory() as session:
            stmt = select(Users).where(Users.username == username)
            user = await session.execute(stmt)
            return user.scalar_one().convert_to_pydantic_model()

    async def get_last_publication_time_by_user_id(self, user_id: int) -> datetime.datetime:
        async with self._async_session_factory() as session:
            stmt = select(Users.last_publication_time).where(Users.id == user_id)
            last_publication_time = await session.execute(stmt)
            return last_publication_time.scalar_one()

    async def set_last_publication_time_by_user_id(
            self,
            user_id: int,
            last_publication_time:
            datetime.datetime
    ) -> dict:
        async with self._async_session_factory() as session:
            stmt = update(Users).where(Users.id == user_id).values(last_publication_time=last_publication_time)
            await session.execute(stmt)
            await session.commit()
            return {
                "message": "successful",
                "detail": f"last publication time for user with id {user_id} set on {last_publication_time}"
            }


def sqlalchemy_users_repository_factory():
    return SQLAlchemyUsersRepository()
