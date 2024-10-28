from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from modules.user.schemas import UserForRegistrate, UserForAuthorize


user_router = APIRouter()


templates = Jinja2Templates(directory="templates")


@user_router.get("/id/{user_id}")
def user_cabinet(user_id, request: Request):
    return templates.TemplateResponse(request=request, name="cabinet.html", context={"id": user_id})


@user_router.get("/registration")
def get_registration_page(request: Request):
    return templates.TemplateResponse(request=request, name="registration.html")


@user_router.post("/registrate-user")
def registrate_user(user_for_registrate: UserForRegistrate):
    print(f"Зарегистрировать чела с данными: \n"
          f"Имя: {user_for_registrate.first_name} \n"
          f"Фамилия: {user_for_registrate.second_name} \n"
          f"Никнейм: {user_for_registrate.username} \n"
          f"Email: {user_for_registrate.email} \n"
          f"Пароль: {user_for_registrate.password} \n")


@user_router.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@user_router.post("/authorize-user")
def authorize_user(user_for_authorize: UserForAuthorize):
    data = {"email": user_for_authorize.email,
            "password": user_for_authorize.password}
    print(f"Данные пользователя, которого нужно авторизовать, ну и проверить: \n"
          f"\n"
          f"{data}")
