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

    auth_service = auth_service_factory()

    async def registrate_user(self, new_user: UserAddSchema):
        try:
            non_hashed_password = new_user.password
            new_user.password = self.auth_service.hash_password(non_hashed_password)
            new_user_id = await self.users_repository.add_user(user=new_user)
            return new_user_id
        except (OSError, InterfaceError):
            print("services/users/users.py/registrate_user --- Нет соединения с БД.")
            raise DatabaseLoseConnection()
        except ProgrammingError:
            print("services/users/users.py/registrate_user --- Нарушение консистентности..")
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

    async def authenticate_user(self, email, password, response: Response):

        try:
            user = await self.users_repository.get_user_by_email(email=email)
        except NoResultFound:
            raise IncorrectCredentialsError()

        if not self.auth_service.validate_password(password, user.password):
            raise IncorrectCredentialsError()

        try:
            await self.tokens_repository.delete_token_by_user_id(user_id=user.id)
        except (OSError, InterfaceError):
            raise DatabaseLoseConnection()

        access_token = self.auth_service.create_access_token(user=user)
        refresh_token = self.auth_service.create_refresh_token(user=user)

        response.set_cookie(key="access-token", value=access_token)
        response.set_cookie(key="refresh-token", value=refresh_token)

        await self.tokens_repository.add_token(token=TokenSchema(refresh_token=refresh_token, user_id=user.id))

    async def logout(self, response: Response, request: Request):
        await self.auth_service.is_user_authorized(request=request, response=response)
        user_id = await self.auth_service.get_user_id_from_jwt(request=request)
        await self.tokens_repository.delete_token_by_user_id(user_id=user_id)


def users_service_factory():
    return UsersService()
