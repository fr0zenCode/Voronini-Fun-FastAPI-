import uuid

from fastapi import Response

from redis_client.utils import insert_key_value_data_in_redis


def generate_session_id() -> str:
    return str(uuid.uuid4())

async def set_session_id_in_cookie(response: Response, session_id: str):
    response.set_cookie(key="session", value=session_id)

async def insert_session_in_redis(user_id: int):
    session_id = generate_session_id()
    await insert_key_value_data_in_redis(key=session_id, value=user_id)
    return session_id
