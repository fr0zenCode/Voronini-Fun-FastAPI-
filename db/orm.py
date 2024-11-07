from sqlalchemy import text

from db.database import async_engine, async_session_factory
from db.models import Base, Posts


class AsyncORM:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_post(author: str, post_text: str):
        new_post = Posts(
            author=author,
            text=post_text
        )

        async with async_session_factory() as session:
            session.add(new_post)
            await session.commit()

    @staticmethod
    async def get_posts():
        async with async_session_factory() as session:
            stmt = text("""SELECT * FROM posts;""")
            result = await session.execute(stmt)
            objs = result.fetchall()
            print(objs)
            return objs
