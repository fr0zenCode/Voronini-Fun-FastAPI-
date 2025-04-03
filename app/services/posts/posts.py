from database.posts.repository.abstract import AbstractPostsRepository
from database.posts.repository.sqlalchemy import sqlalchemy_posts_repository_factory
from database.posts.schemas import AddPostSchema, PostSchema
from .abstract import AbstractPostsService


class PostsService:

    def __init__(self):
        self.posts_repository: AbstractPostsRepository = sqlalchemy_posts_repository_factory()

    async def add_post(self, post: AddPostSchema) -> int:
        new_post_id = await self.posts_repository.add_post(post=post)
        return new_post_id

    async def delete_post(self, post_id: int):
        await self.posts_repository.delete_post_by_id(post_id=post_id)

    async def get_post_by_id(self, post_id: int) -> PostSchema:
        post = await self.posts_repository.get_post_by_id(post_id=post_id)
        return post

    async def get_all_posts(self):
        posts = await self.posts_repository.get_all_posts()
        return posts


def posts_service_factory() -> PostsService:
    return PostsService()
