from typing import Annotated

from fastapi import APIRouter, Request, Depends
from starlette.responses import Response, RedirectResponse

from database.repositories.users.schemas import UsersCredentialsForLogin, UserAddSchema
from services.auth.auth import AuthService, auth_service_factory
from services.users.users import UsersService, users_service_factory


user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/me")
async def user_cabinet(
        response: Response,
        request: Request,
        auth_service: Annotated[AuthService, Depends(auth_service_factory)],
        users_service: Annotated[UsersService, Depends(users_service_factory)]
) -> dict:

    access_token = await auth_service.is_user_authorized(access_token=request.cookies.get("jwt"),
                                                         refresh_token=request.cookies.get("jwt_refresh_token"))

    response.set_cookie(key=auth_service.ACCESS_TOKEN_COOKIES_ALIAS, value=access_token)

    user_id = auth_service.convert_jwt_to_read_format(jwt=access_token)["id"]
    user = await users_service.get_user_by_id(user_id=user_id)

    return {
        "status": "success",
        "data": {
            "user": user
        }
    }


@user_router.post("/registrate-user")
async def registrate_user(
        user_for_registrate: UserAddSchema,
        users_service: Annotated[UsersService, Depends(users_service_factory)]
) -> dict:
    new_user_id = await users_service.registrate_user(user_for_registrate)
    return {
        "status": "success",
        "data": {
            "id": new_user_id,
            "name": f"{user_for_registrate.first_name} {user_for_registrate.second_name}",
            "email": user_for_registrate.email
        }
    }


@user_router.post("/authenticate-user")
async def authenticate_user(
        users_credentials: UsersCredentialsForLogin,
        users_service: Annotated[UsersService, Depends(users_service_factory)],
        response: Response
) -> dict:

    tokens = await users_service.authenticate_user(
        email=users_credentials.email,
        password=users_credentials.password,
    )

    response.set_cookie("jwt", tokens.get("access_token"), httponly=True)
    response.set_cookie("jwt_refresh_token", tokens.get("refresh_token"), httponly=True)

    return {
        "status": "success",
        "data": {
            "detail": "access and refresh tokens set in cookies"
        }
    }


@user_router.post("/logout")
async def logout(
        response: Response,
        request: Request,
        auth_service: Annotated[AuthService, Depends(auth_service_factory)]
) -> dict:

    access_token = await auth_service.is_user_authorized(access_token=request.cookies.get("jwt"),
                                                         refresh_token=request.cookies.get("jwt-refresh-token"))
    response.set_cookie("jwt", access_token)
    user_id = await auth_service.get_user_id_from_jwt(request)

    await auth_service.delete_token_from_db_by_user_id(user_id=user_id)

    response.delete_cookie("jwt")
    response.delete_cookie("jwt_refresh_token")

    return {
        "status": "success",
        "detail": "user has been logged out"
    }
