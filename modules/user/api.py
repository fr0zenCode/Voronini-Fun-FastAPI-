import datetime
import json

import jwt
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
from starlette.responses import Response, JSONResponse

from auth.crud import tokens_crud
from auth.utils import check_cookie_for_refresh_jwt_token
import auth.utils
from auth.tokens import create_refresh_token, create_access_token
from modules.user.schemas import UserForRegistrate, UserForLogin
from config import settings
from .crud import user_crud

user_router = APIRouter()

templates = Jinja2Templates(directory="templates")

http_bearer = HTTPBearer()


@user_router.get("/me")
async def user_cabinet(
        response: Response,
        request: Request,
        jwt_tokens=Depends(auth.utils.check_cookie)
):

    try:
        decoded_jwt = jwt.decode(
            jwt_tokens,
            key=settings.auth_jwt.public_key_path.read_text(),
            algorithms=[settings.auth_jwt.algorithm]
        )
        context = {
           "user_id": decoded_jwt["sub"],
           "username": decoded_jwt["username"],
           "email": decoded_jwt["email"]
        }

        return templates.TemplateResponse(request=request, name="cabinet.html", context=context, status_code=200)

    except jwt.exceptions.ExpiredSignatureError:
        jwt_refresh_token = check_cookie_for_refresh_jwt_token(request)
        decoded_jwt_refresh_token = jwt.decode(
            jwt_refresh_token,
            key=settings.auth_jwt.public_key_path.read_text(),
            algorithms=[settings.auth_jwt.algorithm]
        )
        if decoded_jwt_refresh_token['exp'] > datetime.datetime.now().timestamp():
            user_id = decoded_jwt_refresh_token['sub']
            # запрос к бд, если такой есть, то установить новый акцес, если нет, то респонс как в элсе
            user_object = await user_crud.get_user_by_id(user_id)

                # сделать запрос к токенам, надо создавать токен круд...

            res = await tokens_crud.get_refresh_token_by_user_id(user_id=user_id)

            jwt_refresh_from_db = res['refresh_token']

            if jwt_refresh_token == jwt_refresh_from_db:
                print("Привет")
                access_token = create_access_token(user_object)
                response.set_cookie(key="jwt", value=access_token)

            else:
                print('ERROR:::::modules/user/api/def user cabinet переданного рефреш токена нет в бд')

        else:
            response = templates.TemplateResponse("login.html", {"request": request})
            response.delete_cookie("jwt")
            response.delete_cookie("jwt_refresh_token")
            return response


@user_router.get("/registration")
def get_registration_page(request: Request):
    return templates.TemplateResponse(request=request, name="registration.html")


@user_router.post("/registrate-user")
async def registrate_user(user_for_registrate: UserForRegistrate):

    registration_status = await user_crud.add_user_to_db(
        first_name=user_for_registrate.first_name,
        second_name=user_for_registrate.second_name,
        username=user_for_registrate.username,
        email=user_for_registrate.email,
        password=auth.utils.hash_password(user_for_registrate.password)
    )

    if registration_status == {"message": "successful"}:
        return JSONResponse(content={"message": "successful"}, media_type='application/json', status_code=200)

    if registration_status["message"] == "unsuccessful":
        d = registration_status
        json_str = json.dumps(d)
        return JSONResponse(content=json_str, media_type='application/json', status_code=400)


@user_router.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", status_code=200)


@user_router.post("/authorize-user")
async def authorize_user(response: Response, user_for_login: UserForLogin):

    user = await user_crud.get_user_by_email(email=user_for_login.email)

    if not user:
        return JSONResponse(content={"message": "invalid login or password"}, status_code=304)
    else:
        if not auth.utils.validate_password(user_for_login.password, user.password):
            print("Неправильные логин и пароль")
            return JSONResponse(content={"message": "invalid login or password"}, status_code=304)

        access_token = create_access_token(user)
        response.set_cookie(key="jwt", value=access_token)

        if await tokens_crud.is_refresh_token_exists(user.user_id):
            ...
        else:
            refresh_token = create_refresh_token(user)
            response.set_cookie(key="jwt_refresh_token", value=refresh_token, httponly=True)
            await tokens_crud.add_refresh_jwt_token_to_db(user_id=user.user_id, refresh_jwt_token=refresh_token)


@user_router.post("/logout")
async def logout(request: Request):
    response = templates.TemplateResponse("login.html", {"request": request})
    response.delete_cookie("jwt")
    return response
