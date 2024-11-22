from typing import Callable

from sqlalchemy import text

from db.database import async_session_factory
from modules.post.schemas import PostInfo, PostFromDB
from db.models import Posts


class PostCRUD:

    def __init__(self, session_factory: Callable = async_session_factory()):
        self._session_factory = session_factory

    def get_session_factory(self):
        return self._session_factory()

    async def get_more_posts(self, offset: int, limit: int):
        async with self._session_factory() as session:
            stmt = text("""SELECT * FROM posts 
            ORDER BY posts.created_at DESC 
            LIMIT :limit 
            OFFSET :offset;
            """)
            posts = await session.execute(stmt, {
                "limit": limit,
                "offset": offset
            })
            available_posts = [
                PostFromDB(
                    author_username=res[2], author_id=res[-1], text=res[1], created_at=res[3], post_id=res[0]
                ) for res in posts
            ]
            return available_posts

    async def add_post(self, post: PostInfo):
        new_post = Posts(
            author_username=post.author_username,
            author_id=post.author_id,
            text=post.text,
            created_at=post.created_at
        )

        async with self._session_factory() as session:
            session.add(new_post)
            await session.commit()
        return {"message": "complete"}

    async def delete_post_by_id(self, post_for_delete_id):
        async with self._session_factory() as session:
            stmt = text("""DELETE FROM posts WHERE posts.id=:post_for_delete_id;""")
            await session.execute(stmt, {
                "post_for_delete_id": post_for_delete_id
            })
            await session.commit()

    async def select_posts(self):
        async with self._session_factory() as session:

            stmt = text("""SELECT * FROM posts;""")
            result = await session.execute(stmt)
            available_posts = [
                PostFromDB(
                    author_username=res[2], author_id=res[-1], text=res[1], created_at=res[3], post_id=res[0]
                ) for res in result
            ]
            return available_posts


post_crud = PostCRUD(async_session_factory)
