import uuid

from fastapi import Response

def generate_session_id() -> str:
    return str(uuid.uuid4())

async def set_session_in_cookie(response: Response, session_id: str):
    response.set_cookie(key="session", value=session_id, httponly=True) # todo: вынести в алиас
