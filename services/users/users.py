from dataclasses import dataclass

from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.exc import ProgrammingError, InterfaceError, IntegrityError, NoResultFound

from database.errors import (DatabaseLoseConnection,
                             DatabaseTablesErrors,
                             UserWithTheSameUsernameIsAlreadyExistsError,
                             UserWithTheSameEmailIsAlreadyExistsError,
                             DatabaseColumnsErrors)
from database.tokens.repository.sqlalchemy import sqlalchemy_tokens_repository_factory
from database.tokens.schemas import TokenSchema
from database.users.repository.sqlalchemy import sqlalchemy_users_repository_factory
from database.users.schemas import UserAddSchema
from services.auth.auth import auth_service_factory
from services.auth.cookies import cookies_manager_factory
from services.auth.core import hash_password
from services.users.errors import IncorrectCredentialsError


@dataclass
class UsersService:

    users_repository = sqlalchemy_users_repository_factory()
    tokens_repository = sqlalchemy_tokens_repository_factory()

    auth_service = auth_service_factory()
    cookies_manager = cookies_manager_factory()

    async def registrate_user(self, new_user: UserAddSchema):
        try:
            non_hashed_password = new_user.password
            new_user.password = hash_password(non_hashed_password)
            new_user_id = await self.users_repository.add_user(user=new_user)
            return new_user_id
        except (OSError, InterfaceError):
            raise DatabaseLoseConnection()
        except ProgrammingError:
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

        await self.cookies_manager.set_token_to_cookies(
            token=access_token,
            alias_for_token=self.cookies_manager.ACCESS_TOKEN_COOKIES_ALIAS,
            response=response
        )

        await self.cookies_manager.set_token_to_cookies(
            token=refresh_token,
            alias_for_token=self.cookies_manager.REFRESH_TOKEN_COOKIES_ALIAS,
            response=response
        )

        await self.tokens_repository.add_token(token=TokenSchema(refresh_token=refresh_token, user_id=user.id))

    async def logout(self, response: Response, request: Request):
        await self.auth_service.is_user_authorized(request=request, response=response)
        await self.tokens_repository.delete_token_by_user_id(self.auth_service.get_user_id_from_jwt(request=request))
        await self.tokens_repository.delete_token_by_user_id()
        await self.cookies_manager.delete_token_from_cookies(
            alias_for_token=self.auth_service.ACCESS_TOKEN_COOKIES_ALIAS,
            response=response
        )
        await self.cookies_manager.delete_token_from_cookies(
            alias_for_token=self.auth_service.REFRESH_TOKEN_COOKIES_ALIAS,
            response=response
        )


def users_service_factory():
    return UsersService()
