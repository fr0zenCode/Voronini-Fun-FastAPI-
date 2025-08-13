import uuid

from fastapi import Response

from users.aliases import SESSION_KEY_IN_COOKIES


def generate_session_id() -> str:
    return str(uuid.uuid4())

async def set_session_in_cookie(response: Response, session_id: str):
    response.set_cookie(key=SESSION_KEY_IN_COOKIES, value=session_id, httponly=True)
