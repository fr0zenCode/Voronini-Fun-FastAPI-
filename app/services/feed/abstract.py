from abc import ABC, abstractmethod

from database.posts.schemas import PostSchema


class AbstractFeedService(ABC):

    @abstractmethod
    async def get_posts_portion(self, limit: int, offset: int) -> [PostSchema]:
        ...
