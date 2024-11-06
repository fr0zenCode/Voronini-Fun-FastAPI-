import jwt
from fastapi import APIRouter, Request, Depends, Header
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import Response

import auth.utils
from modules.user.schemas import UserForRegistrate, UserForLogin
from db.orm import AsyncORM
from config import settings

user_router = APIRouter()

templates = Jinja2Templates(directory="templates")

http_bearer = HTTPBearer()


@user_router.get("/me")
def user_cabinet(
        jwt_token=Depends(auth.utils.check_cookie)
):
    decoded_jwt = jwt.decode(
        jwt_token,
        key=settings.auth_jwt.public_key_path.read_text(),
        algorithms=[settings.auth_jwt.algorithm]
    )
    return {
        "username": decoded_jwt["username"],
        "email": decoded_jwt["email"]
    }


@user_router.get("/id/{user_id}")
def user_cabinet(user_id, request: Request, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    decoded_jwt = jwt.decode(
        jwt=credentials.credentials,
        key=settings.auth_jwt.public_key_path.read_text(),
        algorithms=[settings.auth_jwt.algorithm]
    )
    print(decoded_jwt)
    return templates.TemplateResponse(request=request, name="cabinet.html", context={"id": user_id})


@user_router.get("/registration")
def get_registration_page(request: Request):
    return templates.TemplateResponse(request=request, name="registration.html")


@user_router.post("/registrate-user")
async def registrate_user(user_for_registrate: UserForRegistrate):

    try:
        await AsyncORM.add_user_to_db(
            first_name=user_for_registrate.first_name,
            second_name=user_for_registrate.second_name,
            username=user_for_registrate.username,
            email=user_for_registrate.email,
            password=auth.utils.hash_password(user_for_registrate.password)
        )
        print("Зарегали")
    except Exception:
        print("Ошибка", Exception)


@user_router.get("/login")
def get_login_page(request: Request):
    token = Header(alias="Bearer")
    print(token)
    return templates.TemplateResponse(request=request, name="login.html")


def create_access_token(user):
    jwt_payload = {
        "sub": user["user_id"],
        "username": user["username"],
        "email": user["email"]
    }
    access_token = auth.utils.encode_jwt(payload=jwt_payload)
    return access_token


@user_router.post("/authorize-user")
async def authorize_user(response: Response, user_for_login: UserForLogin):

    user = await AsyncORM.select_users(email=user_for_login.email)

    if not user:
        print("Такого нет")
        return None
    else:
        if not auth.utils.validate_password(user_for_login.password, user["password"]):
            print("Неправильные логин и пароль")
            return None
        access_token = create_access_token(user)
        refresh_token = ...
        response.set_cookie("jwt", access_token)
        return {"message": "Я тебя запомнил"}
