import bcrypt
import jwt
from datetime import datetime, timedelta

from starlette.requests import Request

from auth.crud import tokens_crud
from auth.tokens import create_access_token
from config import settings
from modules.user.crud import user_crud


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()

    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


def check_cookie(session_id: str = Cookie(alias="jwt")):
    return session_id
def decode_jwt_token(
        jwt_token,
        key=settings.auth_jwt.public_key_path.read_text(),
        algorithm=settings.auth_jwt.algorithm
):
    decoded_jwt_token = jwt.decode(
        jwt=jwt_token,
        key=key,
        algorithms=[algorithm]
    )
    return decoded_jwt_token


async def check_cookie(request: Request):
    access_token = request.cookies.get("jwt")
    refresh_token = request.cookies.get("jwt_refresh_token")

    if not access_token or not refresh_token:
        print("ERROR: "
              "auth/utils/check_cookie ----> "
              "в куках не нашлось рефреш или акцес токена. Необходимо заново авторизоваться.")
        return "FALSE"

    try:
        decode_jwt_token(access_token)
        print("INFO: auth/utils/check_cookie ----> все хорошо, ничего делать не надо.")
        return "TRUE"

    except jwt.exceptions.ExpiredSignatureError:
        print("INFO: auth/utils/check_cookie ----> акцес токен просрочен")

        try:
            decoded_refresh_token = decode_jwt_token(refresh_token)
            refresh_token_from_db = await tokens_crud.get_refresh_token_by_user_id(decoded_refresh_token["sub"])
            if refresh_token_from_db["refresh_token"] != refresh_token:
                print("ERROR: "
                      "auth/utils/check_cookie ----> "
                      "рефреш токен просрочен или не совпадает с токеном в БД. Необходимо заново авторизоваться.")
                return "FALSE"

            print("INFO: auth/utils/check_cookie ----> создаем новый акцесс токен по рефреш токену")
            user = await user_crud.get_user_by_id(decoded_refresh_token["sub"])
            new_access_token = create_access_token(user)
            return new_access_token

        except jwt.exceptions.ExpiredSignatureError:
            return "FALSE"
