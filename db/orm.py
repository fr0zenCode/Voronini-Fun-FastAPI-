from sqlalchemy import text

from db.database import async_engine, async_session_factory
from db.models import Users, Base


class AsyncORM:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def add_user_to_db(first_name, second_name, username, email, password, is_active=True):
        user = Users(
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
    async def select_users(email, password):
        async with (async_session_factory() as session):
            stmt = text("""SELECT * FROM users WHERE users.email=:email and users.password=:password;""")
            result = await session.execute(stmt, {
                "email": email,
                "password": password
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
