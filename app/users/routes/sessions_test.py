from typing import Final

from fastapi import APIRouter, Response

TEST_SESSION_COOKIE_ALIAS: Final = "session"

sessions_test_router = APIRouter(prefix="/sessions/test", tags=["sessions test"])

@sessions_test_router.post(
    path="/set-session-in-cookie/",
    summary="This api sets 'session' with input data to cookies"
)
async def set_session_in_cookie(response: Response, session_fake_id: str) -> None:
    response.set_cookie(key=TEST_SESSION_COOKIE_ALIAS, value=session_fake_id)
