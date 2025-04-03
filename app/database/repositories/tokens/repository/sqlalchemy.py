from dataclasses import dataclass

from sqlalchemy import insert, select, delete

from database.core.database import async_session_factory
from database.core.models import Tokens
from database.repositories.tokens.repository.abstract import AbstractTokensRepository
from database.repositories.tokens.schemas import TokenSchema


@dataclass
class SQLAlchemyTokensRepository(AbstractTokensRepository):

    _async_session_factory = async_session_factory

    async def add_token(self, token: TokenSchema) -> dict:
        async with self._async_session_factory() as session:
            stmt = insert(Tokens).values(
                user_id=token.user_id,
                refresh_token=token.refresh_token
            )
            await session.execute(stmt)
            await session.commit()
            return {
                "message": "successful",
                "detail": "token added to database"
            }

    async def is_token_for_user_exists_by_user_id(self, user_id: int) -> bool:
        async with self._async_session_factory() as session:
            stmt = select(Tokens).where(Tokens.user_id == user_id)
            token = await session.execute(stmt)
            if token.scalars():
                return True
            return False

    async def get_token_by_user_id(self, user_id: int) -> TokenSchema:
        async with self._async_session_factory() as session:
            stmt = select(Tokens).where(Tokens.user_id == user_id)
            token = await session.execute(stmt)
            return token.scalar_one().convert_to_pydantic_model()

    async def delete_token_by_user_id(self, user_id: int) -> dict:
        async with self._async_session_factory() as session:
            stmt = delete(Tokens).where(Tokens.user_id == user_id)
            await session.execute(stmt)
            await session.commit()
            return {
                "message": "successful",
                "detail": f"token for user with id {user_id} deleted"
            }


def sqlalchemy_tokens_repository_factory():
    return SQLAlchemyTokensRepository()
