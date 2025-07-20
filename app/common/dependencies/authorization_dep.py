from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyCookie\

SessionIDCookie = Annotated[
    str | None,
    Depends(
        APIKeyCookie(
            name="session",
            auto_error=False,
            scheme_name="current user session cookie"
        )
    )
]

async def session_id_proxy(
        session_id: SessionIDCookie
) -> str:
    return session_id

SessionID = Annotated[str, Depends(session_id_proxy)]
