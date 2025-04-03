from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.exc import ProgrammingError, InterfaceError, IntegrityError, NoResultFound

from database.errors import (DatabaseLoseConnection,
                             DatabaseTablesErrors,
                             UserWithTheSameUsernameIsAlreadyExistsError,
                             UserWithTheSameEmailIsAlreadyExistsError,
                             DatabaseColumnsErrors)
from database.repositories.tokens.repository.sqlalchemy import sqlalchemy_tokens_repository_factory
from database.repositories.tokens.schemas import TokenSchema
from database.repositories.users.repository.sqlalchemy import sqlalchemy_users_repository_factory
from database.repositories.users.schemas import UserAddSchema, UserSchema
from services.users.errors import IncorrectCredentialsError
from logger import logger


class UsersService:

    def __init__(self):
        self.users_repository = sqlalchemy_users_repository_factory()
        self.tokens_repository = sqlalchemy_tokens_repository_factory()

    async def registrate_user(self, new_user: UserAddSchema) -> int:
        """
        :param new_user: ``UserAddSchema`` данные пользователя, упакованные в Pydantic-class
        :return: ``int`` new_user_id
        """
        from services.auth.auth import auth_service_factory
        auth_service = auth_service_factory()

        try:
            non_hashed_password = new_user.password
            new_user.password = auth_service.hash_password(non_hashed_password)
            new_user_id = await self.users_repository.add_user(user=new_user)
            return new_user_id
        except (OSError, InterfaceError):
            logger.error("Нет соединения с БД.")
            raise DatabaseLoseConnection()
        except ProgrammingError:
            logger.error("Нарушение консистенции.")
            raise DatabaseTablesErrors()
        except IntegrityError:

            try:
                if await self.users_repository.get_user_by_username(username=new_user.username):
                    raise UserWithTheSameUsernameIsAlreadyExistsError()
            except NoResultFound:
                ...

            try:
                if await self.users_repository.get_user_by_email(email=new_user.email):
                    raise UserWithTheSameEmailIsAlreadyExistsError()
            except NoResultFound:
                ...

            raise DatabaseColumnsErrors()

    async def authenticate_user(self, email, password) -> dict[str, str]:
        """
        В функцию передаются email и пароль пользователя. В случае, если функция не вызвала никакого исключения,
        данные пользователя считаются аутентичными.

        **return example:** \n
            {
                "access_token": access_token, \n
                "refresh_token": refresh_token \n
            }
        """
        from services.auth.auth import auth_service_factory
        auth_service = auth_service_factory()
        try:
            user = await self.users_repository.get_user_by_email(email=email)
        except NoResultFound:
            raise IncorrectCredentialsError()

        if not auth_service.validate_password(password, user.password):
            raise IncorrectCredentialsError()

        try:
            await self.tokens_repository.delete_token_by_user_id(user_id=user.id)
        except (OSError, InterfaceError):
            raise DatabaseLoseConnection()

        access_token = auth_service.create_access_token(user=user)
        refresh_token = auth_service.create_refresh_token(user=user)

        await self.tokens_repository.add_token(TokenSchema(user_id=user.id, refresh_token=refresh_token))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    async def logout(self, response: Response, request: Request):
        """
        Если пользователь авторизован, то функция удаляет его токен из базы данных.
        """
        from services.auth.auth import auth_service_factory
        auth_service = auth_service_factory()
        await auth_service.is_user_authorized(request=request, response=response)
        user_id = await auth_service.get_user_id_from_jwt(request=request)
        await self.tokens_repository.delete_token_by_user_id(user_id=user_id)


def users_service_factory():
    return UsersService()
