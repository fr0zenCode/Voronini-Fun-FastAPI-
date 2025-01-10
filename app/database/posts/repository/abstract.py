from abc import ABC, abstractmethod

from database.posts.schemas import AddPostSchema, PostSchema


class AbstractPostsRepository(ABC):

    @abstractmethod
    async def add_post(self, post: AddPostSchema) -> int:
        ...

    @abstractmethod
    async def delete_post_by_id(self, post_id: int) -> dict:
        ...

    @abstractmethod
    async def get_more_posts(self, offset: int, limit: int) -> list[PostSchema]:
        ...

    @abstractmethod
    async def get_all_posts(self) -> list[PostSchema]:
        ...

    @abstractmethod
    async def get_post_by_id(self, post_id: int) -> PostSchema:
        ...
