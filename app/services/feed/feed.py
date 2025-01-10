from database.posts.repository.abstract import AbstractPostsRepository
from database.posts.repository.sqlalchemy import sqlalchemy_posts_repository_factory
from database.posts.schemas import PostSchema
from services.feed.abstract import AbstractFeedService


class FeedService(AbstractFeedService):

    def __init__(self):
        self.posts_repository: AbstractPostsRepository = sqlalchemy_posts_repository_factory()

    async def get_posts_portion(self, limit: int, offset: int) -> [PostSchema]:
        posts = await self.posts_repository.get_more_posts(limit=limit, offset=offset)
        return posts


def feed_service_factory() -> FeedService:
    return FeedService()
