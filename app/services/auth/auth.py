from dataclasses import dataclass
from datetime import timedelta

import bcrypt
from jwt import ExpiredSignatureError
from starlette.requests import Request

from database.tokens.repository.sqlalchemy import sqlalchemy_tokens_repository_factory
from database.tokens.schemas import TokenSchema
from database.users.repository.sqlalchemy import sqlalchemy_users_repository_factory
from database.users.schemas import UserSchema
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

    def validate_password(self, regular_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=regular_password.encode(self.ENCODING_TYPE),
            hashed_password=hashed_password.encode(self.ENCODING_TYPE)
        )

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        password_bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)

    def create_access_token(self, user: UserSchema) -> str:
        jwt_payload = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }
        access_token = create_jwt_token(
            token_type=self.ACCESS_TOKEN_TYPE_POINTER,
            payload=jwt_payload,
            expire_timedelta=timedelta(minutes=5)
        )
        return access_token

    def create_refresh_token(self, user: UserSchema) -> str:
        jwt_payload = {"user_id": user.id}
        refresh_token = create_jwt_token(
            token_type=self.REFRESH_TOKEN_TYPE_POINTER,
            payload=jwt_payload,
            expire_timedelta=timedelta(days=7)
        )
        return refresh_token

    async def add_refresh_token_to_database(self, refresh_token_schema: TokenSchema):
        await self.tokens_repository.add_token(token=refresh_token_schema)

    @staticmethod
    def is_token_alive(token: str, refresh_token_mode: bool = False) -> bool:
        try:
            decode_jwt(token)
            return True
        except ExpiredSignatureError:
            if refresh_token_mode:
                print("refresh-token тоже просрочен. Необходимо заново аутентифицироваться.")
                raise UserNotAuthorizedError()
            return False

    @staticmethod
    async def convert_jwt_to_read_format(jwt: str) -> dict:
        decoded_jwt = decode_jwt(jwt)
        return {
            "id": decoded_jwt["user_id"],
            "username": decoded_jwt["username"],
            "email": decoded_jwt["email"]
        }

    async def get_user_id_from_jwt(self, request: Request):
        access_token = request.cookies.get(self.ACCESS_TOKEN_COOKIES_ALIAS)
        return decode_jwt(jwt_for_decode=access_token)["user_id"]

    async def create_access_token_by_refresh_token(self, refresh_token: str):
        decoded_refresh_token = decode_jwt(refresh_token)
        user_id = decoded_refresh_token["user_id"]
        await self.compare_refresh_token_with_database_version(refresh_token=refresh_token, user_id=user_id)
        user = await self.users_repository.get_user_by_id(user_id)
        new_access_token = self.create_access_token(user)
        return new_access_token

    async def compare_refresh_token_with_database_version(self, refresh_token: str, user_id: int):
        refresh_token_model_from_db = await self.tokens_repository.get_token_by_user_id(user_id=user_id)
        if refresh_token_model_from_db.refresh_token == refresh_token:
            return True
        print("refresh-token из cookies не совпал с токеном из Базы Данных. Приходется пройти процедуру аутенификации.")
        raise UserNotAuthorizedError()

    async def is_user_authorized(self, access_token: str, refresh_token: str):

        if self.is_token_alive(token=access_token, refresh_token_mode=False):
            print("access-token действителен, ничего не требуется. Продолжаем.")
            return access_token

        print("access-token просрочен. Проверяем возможность генерации нового на основании refresh-token'a.")

        if self.is_token_alive(token=refresh_token, refresh_token_mode=True):

            print("refresh-token действителен. Начинаем создание нового access-token'a.")

            user_id = decode_jwt(refresh_token)["user_id"]
            await self.compare_refresh_token_with_database_version(refresh_token=refresh_token, user_id=user_id)
            print("Соответствие refresh-token'a с токеном из БД подтверждено.")
            new_access_token = await self.create_access_token_by_refresh_token(refresh_token)
            print("Новый access-token создан.")
            return new_access_token

        print("refresh-token также просрочен. Приходется пройти процедуру аутентификации.")


def auth_service_factory():
    return AuthService()
