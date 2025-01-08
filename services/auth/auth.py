from dataclasses import dataclass
from datetime import timedelta

import bcrypt
from starlette.requests import Request
from starlette.responses import Response

from database.tokens.repository.sqlalchemy import sqlalchemy_tokens_repository_factory
from database.tokens.schemas import TokenSchema
from database.users.repository.sqlalchemy import sqlalchemy_users_repository_factory
from database.users.schemas import UserSchema
from .cookies import cookies_manager_factory
from .core import decode_jwt, create_jwt_token
from ..users.errors import UserNotAuthorizedError


@dataclass
class AuthService:

    ACCESS_TOKEN_COOKIES_ALIAS = "access-token"
    REFRESH_TOKEN_COOKIES_ALIAS = "refresh-token"

    ACCESS_TOKEN_TYPE_POINTER = "access"
    REFRESH_TOKEN_TYPE_POINTER = "refresh"

    ENCODING_TYPE = "UTF-8"

    tokens_repository = sqlalchemy_tokens_repository_factory()
    users_repository = sqlalchemy_users_repository_factory()
    cookies_manager = cookies_manager_factory()

    @staticmethod
    async def is_token_alive(token: str) -> bool:
        decode_jwt(token)
        return True

    async def add_refresh_token_to_database(self, refresh_token: TokenSchema):
        ...

    async def get_user_id_from_jwt(self, request: Request):
        access_token = await self.cookies_manager.get_token_from_cookies(
            request=request,
            alias_for_token=self.ACCESS_TOKEN_COOKIES_ALIAS
        )
        return decode_jwt(jwt_for_decode=access_token)["id"]

    def validate_password(self, regular_password: str, hashed_password: str) -> bool:
        result = bcrypt.checkpw(
            password=regular_password.encode(self.ENCODING_TYPE),
            hashed_password=hashed_password.encode(self.ENCODING_TYPE)
        )
        return result

    def create_access_token(self, user: UserSchema) -> str:
        jwt_payload = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }
        access_token = create_jwt_token(
            token_type=self.ACCESS_TOKEN_TYPE_POINTER,
            payload=jwt_payload
        )
        return access_token

    def create_refresh_token(self, user: UserSchema) -> str:
        jwt_payload = {"user_id": user.id}
        refresh_token = create_jwt_token(
            token_type=self.REFRESH_TOKEN_TYPE_POINTER,
            payload=jwt_payload,
            expire_timedelta=timedelta(days=30)
        )
        return refresh_token

    async def create_access_token_by_refresh_token(self, refresh_token: str):

        decoded_refresh_token = decode_jwt(refresh_token)
        refresh_token_from_db = await self.tokens_repository.get_token_by_user_id(decoded_refresh_token["id"])

        if refresh_token_from_db["refresh_token"] != refresh_token:
            raise UserNotAuthorizedError()

        user = await self.users_repository.get_user_by_id(decoded_refresh_token["sub"])
        new_access_token = self.create_access_token(user)
        return new_access_token

    async def is_user_authorized(self, request: Request, response: Response) -> Response:

        access_token = await self.cookies_manager.get_token_from_cookies(
            alias_for_token=self.ACCESS_TOKEN_COOKIES_ALIAS, request=request
        )
        refresh_token = await self.cookies_manager.get_token_from_cookies(
            alias_for_token=self.REFRESH_TOKEN_COOKIES_ALIAS, request=request
        )

        if not isinstance(access_token, bytes | str) or not isinstance(refresh_token, bytes | str):
            raise UserNotAuthorizedError()

        if await self.is_token_alive(token=access_token):
            return response

        if await self.is_token_alive(token=refresh_token):

            user_id = decode_jwt(refresh_token)["id"]
            refresh_token_from_db = self.tokens_repository.get_token_by_user_id(user_id=user_id)

            if refresh_token_from_db == refresh_token:
                new_access_token = await self.create_access_token_by_refresh_token(refresh_token)
                response.set_cookie(key=self.ACCESS_TOKEN_COOKIES_ALIAS, value=new_access_token)
                return response

        response.delete_cookie(self.ACCESS_TOKEN_COOKIES_ALIAS)
        response.delete_cookie(self.REFRESH_TOKEN_COOKIES_ALIAS)
        raise UserNotAuthorizedError()


def auth_service_factory():
    return AuthService()
