from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from database.users.schemas import UsersCredentialsForLogin, UserAddSchema
from services.auth.auth import AuthService, auth_service_factory
from services.users.users import UsersService, users_service_factory

user_router = APIRouter(prefix="/user", tags=["User"])

templates = Jinja2Templates(directory="templates")


@user_router.get("/me")
async def user_cabinet(
        response: Response,
        request: Request,
        auth_service: Annotated[AuthService, Depends(auth_service_factory)]
) -> dict:

    access_token = await auth_service.is_user_authorized(access_token=request.cookies.get("access-token"),
                                                         refresh_token=request.cookies.get("refresh-token"))

    response.set_cookie(key=auth_service.ACCESS_TOKEN_COOKIES_ALIAS, value=access_token)

    user_info = await auth_service.convert_jwt_to_read_format(jwt=access_token)

    return user_info


@user_router.post("/registrate-user")
async def registrate_user(
        user_for_registrate: UserAddSchema,
        users_service: Annotated[UsersService, Depends(users_service_factory)]
) -> dict:
    new_user_id = await users_service.registrate_user(user_for_registrate)
    return {"message": f"successfully. Your ID in system is {new_user_id}"}


@user_router.post("/authenticate-user")
async def authenticate_user(
        response: Response,
        users_credentials: UsersCredentialsForLogin,
        users_service: Annotated[UsersService, Depends(users_service_factory)]
) -> dict:
    await users_service.authenticate_user(
        email=users_credentials.email,
        password=users_credentials.password,
        response=response
    )
    return {"message": "successful"}


@user_router.post("/logout")
async def logout(
        response: Response,
        request: Request,
        users_service: Annotated[UsersService, Depends(users_service_factory)]
) -> dict:
    await users_service.logout(request=request, response=response)
    return {"message": "successful"}
