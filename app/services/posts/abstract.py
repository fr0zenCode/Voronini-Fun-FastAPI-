from abc import ABC, abstractmethod

from database.posts.repository.abstract import AbstractPostsRepository
from database.posts.schemas import AddPostSchema


class AbstractPostsService(ABC):

    posts_repository: AbstractPostsRepository

    @abstractmethod
    async def add_post(self, post: AddPostSchema) -> int:
        ...

    @abstractmethod
    async def delete_post(self, post_id: int):
        ...

    @abstractmethod
    async def get_post_by_id(self, post_id: int):
        ...

    @abstractmethod
    async def get_all_posts(self):
        ...
