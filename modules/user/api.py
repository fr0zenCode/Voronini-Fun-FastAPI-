import json

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse, RedirectResponse

from auth.crud import tokens_crud
import auth.utils
from auth.tokens import create_refresh_token, create_access_token
from modules.user.schemas import UserForRegistrate, UserForLogin
from .crud import user_crud

user_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@user_router.get("/me")
async def user_cabinet(
        request: Request
):

    check_cookies_result = await auth.utils.check_cookie(request=request)

    if check_cookies_result == "FALSE":
        response = RedirectResponse(url='/user/login')
        response.delete_cookie("jwt")
        response.delete_cookie("jwt_refresh_token")
        return response

    access_token = ""

    if check_cookies_result == "TRUE":
        access_token = request.cookies.get("jwt")

    if not access_token:
        access_token = check_cookies_result

    decoded_jwt = auth.utils.decode_jwt_token(access_token)

    context = {
        "user_id": decoded_jwt["sub"],
        "username": decoded_jwt["username"],
        "email": decoded_jwt["email"]
    }

    response = templates.TemplateResponse(request=request, name="cabinet.html", context=context, status_code=200)
    response.set_cookie("jwt", access_token)
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
async def authorize_user(user_for_login: UserForLogin):

    user = await user_crud.get_user_by_email(email=user_for_login.email)

    if not user:
        return JSONResponse(content={"message": "invalid login or password"}, status_code=304)
    else:
        if not auth.utils.validate_password(user_for_login.password, user.password):
            print("Неправильные логин и пароль")
            return JSONResponse(content={"message": "invalid login or password"}, status_code=304)

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        await tokens_crud.delete_token_by_user_id(user_id=user.user_id)
        await tokens_crud.add_refresh_jwt_token_to_db(user_id=user.user_id, refresh_jwt_token=refresh_token)

        response = RedirectResponse(url="/feed", status_code=303)
        response.set_cookie("jwt", access_token)
        response.set_cookie("jwt_refresh_token", refresh_token, httponly=True)
        return response


@user_router.post("/logout")
async def logout():
    response = RedirectResponse(url="/user/login")
    response.delete_cookie("jwt")
    response.delete_cookie("jwt_refresh_token")
    return response
