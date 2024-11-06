import uuid

from sqlalchemy import text

from db.database import async_engine, async_session_factory
from db.models import Users, Base, Posts


class AsyncORM:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_user_to_db(first_name, second_name, username, email, password, is_active=True):
        user = Users(
            user_id=str(uuid.uuid4()),
            first_name=first_name,
            second_name=second_name,
            username=username,
            email=email,
            password=password,
            is_active=is_active
        )

        async with async_session_factory() as session:
            session.add(user)
            await session.commit()

    @staticmethod
    async def select_users(email):
        async with async_session_factory() as session:
            stmt = text("""SELECT * FROM users WHERE users.email=:email;""")
            result = await session.execute(stmt, {
                "email": email
            })
            obj = result.first()
            return {
                "user_id": obj[0],
                "first_name": obj[1],
                "second_name": obj[2],
                "username": obj[3],
                "email": obj[4],
                "password": obj[5],
                "is_active": obj[6]
            }

    @staticmethod
    async def get_user_by_username(username: str):
        async with async_session_factory() as session:
            stmt = text("""SELECT * FROM users WHERE users.username="username;""")
            result = await session.execute(stmt, {
                "username": username
            })
            obj = result.first()
            return {
                "user_id": obj[0],
                "first_name": obj[1],
                "second_name": obj[2],
                "username": obj[3],
                "email": obj[4],
                "password": obj[5],
                "is_active": obj[6]
            }

    @staticmethod
    async def deactivate_user(user_id, email, password):
        async with async_session_factory() as session:
            stmt = text("""
            UPDATE users 
            SET users.is_active=False 
            WHERE users.user_id=:user_id 
            and users.email=:email 
            and users.password=:password
            """)
            await session.execute(stmt, {
                "user_id": user_id,
                "email": email,
                "password": password
            })
            return {"message": "User has been deleted"}

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
