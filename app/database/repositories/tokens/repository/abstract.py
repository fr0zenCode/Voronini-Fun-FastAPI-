from abc import ABC, abstractmethod

from database.repositories.tokens.schemas import TokenSchema


class AbstractTokensRepository(ABC):

    @abstractmethod
    async def add_token(self, token: TokenSchema) -> dict:
        ...

    @abstractmethod
    async def is_token_for_user_exists_by_user_id(self, user_id: int) -> bool:
        ...

    @abstractmethod
    async def get_token_by_user_id(self, user_id: int) -> TokenSchema:
        ...

    @abstractmethod
    async def delete_token_by_user_id(self, user_id: int) -> dict:
        ...


