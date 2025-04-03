import datetime
from abc import ABC, abstractmethod

from pydantic import EmailStr

from database.repositories.users.schemas import UserAddSchema, UserSchema


class AbstractUsersRepository(ABC):

    @abstractmethod
    async def add_user(self, user: UserAddSchema) -> int:
        ...

    @abstractmethod
    async def delete_user_by_id(self, user_id: int) -> dict:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserSchema:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> UserSchema:
        ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserSchema:
        ...

    @abstractmethod
    async def get_last_publication_time_by_user_id(self, user_id: int) -> datetime.datetime:
        ...

    @abstractmethod
    async def set_last_publication_time_by_user_id(
            self,
            user_id: int,
            last_publication_time:
            datetime.datetime
    ) -> dict:
        ...
