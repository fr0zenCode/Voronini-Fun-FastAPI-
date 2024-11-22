import asyncio
import os

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings


TABLES_FOR_CLEAN = ["users"]

test_async_engine = create_async_engine(url=settings.test_database_url_asyncpg)
test_async_session_factory = async_sessionmaker(test_async_engine)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    os.system("cd modules/user/tests && alembic init migrations")
    os.system('cd modules/user/tests && alembic revision --autogenerate -m "test running migrations”')
    os.system("cd modules/user/tests && alembic upgrade heads")
    print("Фикстура 'run_migrations()' отработала: создала и применила миграции.")


@pytest.fixture(scope="function")
async def clean_tables():
    session = test_async_session_factory()
    await session.begin()
    for table in TABLES_FOR_CLEAN:
        await session.execute(text(f"""TRUNCATE TABLE {table};"""))
        await session.commit()
    await session.close()
