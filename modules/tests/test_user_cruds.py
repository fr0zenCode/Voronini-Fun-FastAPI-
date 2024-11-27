import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings
from modules.user.crud import UserCRUD

test_async_engine = create_async_engine(url=settings.test_database_url_asyncpg)
test_async_session_factory = async_sessionmaker(test_async_engine)


@pytest.mark.asyncio
async def test_read_user(clean_tables):

    user_crud = UserCRUD(test_async_session_factory)

    registration_message = await user_crud.add_user_to_db(
        first_name="Иван",
        second_name="Иванов",
        email="Ivan@gmail.com",
        username="IvanIvanov",
        password=b"some_hashed_password"
    )
    assert registration_message == {"message": "successful"}

    user = await user_crud.get_user_by_email(email="Ivan@gmail.com")
    assert user.username == "IvanIvanov"

    user_id = user.user_id

    user = await user_crud.get_user_by_id(user_id=user_id)
    assert user.first_name == "Иван"

    user = await user_crud.get_user_by_username("IvanIvanov")
    assert user.user_id == user_id

    await user_crud.delete_user_by_id(user_id=user_id)

    # Очищаем таблицу от тестовых данных
    await clean_tables
