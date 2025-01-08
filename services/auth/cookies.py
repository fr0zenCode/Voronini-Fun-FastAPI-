from dataclasses import dataclass

from starlette.requests import Request
from starlette.responses import Response


@dataclass
class CookiesManager:

    ACCESS_TOKEN_COOKIES_ALIAS = "access-token"
    REFRESH_TOKEN_COOKIES_ALIAS = "refresh_token"

    @staticmethod
    async def delete_token_from_cookies(alias_for_token: str, response: Response) -> Response:
        response.delete_cookie(key=alias_for_token)
        return response

    @staticmethod
    async def set_token_to_cookies(token: str, alias_for_token: str, response: Response) -> Response:
        response.set_cookie(key=alias_for_token, value=token, httponly=True)
        return response

    @staticmethod
    async def get_token_from_cookies(request: Request, alias_for_token: str) -> str:
        token = request.cookies.get(alias_for_token)
        return token


def cookies_manager_factory() -> CookiesManager:
    return CookiesManager()
