import bcrypt
import jwt
from datetime import datetime, timedelta

from fastapi import Cookie

from config import settings


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


def check_cookie_for_refresh_jwt_token(request):
    return request.cookies.get('jwt_refresh_token')
