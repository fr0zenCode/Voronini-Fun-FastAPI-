from dataclasses import dataclass
from datetime import timedelta

import bcrypt
from jwt import ExpiredSignatureError
from starlette.requests import Request

from database.repositories.tokens.repository.sqlalchemy import sqlalchemy_tokens_repository_factory
from database.repositories.tokens.schemas import TokenSchema
from database.repositories.users.repository.sqlalchemy import sqlalchemy_users_repository_factory
from database.repositories.users.schemas import UserSchema
from .core import decode_jwt, create_jwt_token
from ..users.errors import UserNotAuthorizedError
from logger import logger


@dataclass
class AuthService:

    ACCESS_TOKEN_COOKIES_ALIAS = "jwt"
    REFRESH_TOKEN_COOKIES_ALIAS = "jwt_refresh_token"

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

    async def add_refresh_token_to_database(self, refresh_token_schema: TokenSchema) -> None:
        """
        Добавляет refresh-token в базу данных токенов.

        :param refresh_token_schema: **TokenSchema**
        :return: None
        """
        await self.tokens_repository.add_token(token=refresh_token_schema)

    @staticmethod
    def is_token_alive(token: str) -> bool:
        """
        Если функция не инициировала вызов исключения, токен считается действительным. "Под капотом" используется
        функция ``.decode()`` из библиотеки **PyJWT**.

        :param token: **str** - токен для проверки, должен быть JWT токеном, т.к. используется функция **.decode()** из библиотеки **PyJWT**
        :return: **bool** - в случае, когда токен действителен. В обратном случае инициируется исключение.
        """
        try:
            decode_jwt(token)
            return True
        except ExpiredSignatureError:
            logger.info(f"Токен {token} просрочен. Необходимо заново пройти процедуру аутентификации.")
            return False

    @staticmethod
    def convert_jwt_to_read_format(jwt: str) -> dict:
        """
        **return example:** \n
            {
                "id": "random-id-123456", \n
                "username": "ivanov", \n
                "email": "example@email.com" \n
            }
        """
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

    async def compare_refresh_token_with_database_version(self, refresh_token: str, user_id: int) -> bool:
        """
        Сравнивает переданный ``refresh_token`` с refresh_token'ом из базы данных. В базе данных refresh_token
        ищется по переданному ``user_id``.

        :param refresh_token: **str**
        :param user_id: **int**
        :return: True, если токены совпадают; в обратном случае инициируется вызов исключения.
        """
        refresh_token_model_from_db = await self.tokens_repository.get_token_by_user_id(user_id=user_id)
        if refresh_token_model_from_db.refresh_token == refresh_token:
            return True
        logger.info("refresh-token из cookies не совпал с refresh-token'ом из базы данных")
        raise UserNotAuthorizedError()

    async def is_user_authorized(self, access_token: str, refresh_token: str):

        if self.is_token_alive(token=access_token, refresh_token_mode=False):
            print("access-token действителен, ничего не требуется. Продолжаем.")
            logger.debug("access-token действителен, ничего не требуется. Продолжаем.")
            return access_token

        logger.debug("Access-token просрочен. Проверяем возможность генерации нового на основании refresh-token'а.")

        if self.is_token_alive(token=refresh_token):
            logger.debug("refresh-token действителен. Начинаем создание нового access-token'а.")

            user_id = decode_jwt(refresh_token)["user_id"]
            await self.compare_refresh_token_with_database_version(refresh_token=refresh_token, user_id=user_id)

            logger.debug("Соответствие refresh-token'а с токеном из БД подтверждено.")
            new_access_token = await self.create_access_token_by_refresh_token(refresh_token)
            logger.debug("Новый access-token создан.")
            return new_access_token

        logger.debug("Refresh-token также просрочен. Придётся пройти процедуру аутентификации.")


def auth_service_factory():
    return AuthService()
