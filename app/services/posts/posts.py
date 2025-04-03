from database.repositories.posts.repository.abstract import AbstractPostsRepository
from database.repositories.posts.repository.sqlalchemy import sqlalchemy_posts_repository_factory
from database.repositories.posts.schemas import AddPostSchema, PostSchema


class PostsService:

    def __init__(self):
        self.posts_repository: AbstractPostsRepository = sqlalchemy_posts_repository_factory()

    async def add_post(self, post: AddPostSchema) -> int:
        new_post_id = await self.posts_repository.add_post(post=post)
        return new_post_id

    async def delete_post(self, post_id: int) -> None:
        await self.posts_repository.delete_post_by_id(post_id=post_id)

    async def get_post_by_id(self, post_id: int) -> PostSchema:
        post = await self.posts_repository.get_post_by_id(post_id=post_id)
        return post

    async def get_all_posts(self) -> list[PostSchema]:
        posts = await self.posts_repository.get_all_posts()
        return posts

    async def get_portion_of_posts(self, limit: int = 10, offset: int = 10) -> list[PostSchema]:
        posts = await self.posts_repository.get_more_posts(offset=offset, limit=limit)
        return posts


def posts_service_factory() -> PostsService:
    return PostsService()
