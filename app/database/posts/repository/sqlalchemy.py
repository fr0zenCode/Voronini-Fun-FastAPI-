from dataclasses import dataclass

from sqlalchemy import insert, delete, select

from .abstract import AbstractPostsRepository
from ..schemas import AddPostSchema, PostSchema
from ...core.database import async_session_factory
from ...core.models import Posts


@dataclass
class SQLAlchemyPostsRepository(AbstractPostsRepository):

    _async_session_factory = async_session_factory

    async def add_post(self, post: AddPostSchema) -> int:

        async with self._async_session_factory() as session:

            stmt = insert(Posts).values(
                author_username=post.author_username,
                author_id=post.author_id,
                text=post.text_content,
                created_at=post.created_at
            ).returning(Posts.id)

            added_post_id = await session.execute(stmt)
            await session.commit()
            return added_post_id.scalar_one()

    async def delete_post_by_id(self, post_id: int) -> dict:
        async with self._async_session_factory() as session:
            stmt = delete(Posts).where(Posts.id == post_id)
            await session.execute(stmt)
            await session.commit()
            return {"message": f"post with id {post_id} successfully deleted!"}

    async def get_more_posts(self, offset: int, limit: int) -> list[PostSchema]:
        async with self._async_session_factory() as session:
            stmt = select(Posts).limit(limit).offset(offset)
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [row.to_pydantic_model() for row in rows]

    async def get_all_posts(self) -> list[PostSchema]:
        async with self._async_session_factory() as session:
            stmt = select(Posts)
            result = await session.execute(stmt)
            posts = result.scalars().all()
            return [post.to_pydantic_model() for post in posts]

    async def get_post_by_id(self, post_id: int) -> PostSchema:
        async with self._async_session_factory() as session:
            stmt = select(Posts).where(Posts.id == post_id)
            result = await session.execute(stmt)
            post = result.scalar_one().to_pydantic_model()
            return post


def sqlalchemy_posts_repository_factory():
    return SQLAlchemyPostsRepository()
