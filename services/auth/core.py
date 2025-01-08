import datetime
from datetime import timedelta

import bcrypt
import jwt

from database.users.schemas import UserSchema
from app.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
):
    payload_to_encode = payload.copy()
    now = datetime.datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    payload_to_encode.update(exp=expire, iat=now)
    encoded_jwt = jwt.encode(payload_to_encode, private_key, algorithm=algorithm)

    return encoded_jwt


def decode_jwt(
        jwt_for_decode: bytes | str,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    decoded_jwt = jwt.decode(jwt_for_decode, public_key, algorithms=[algorithm])
    return decoded_jwt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)


def create_jwt_token(
    token_type: str,
    payload: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
):

    jwt_payload = {"type": token_type}
    jwt_payload.update(payload)

    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )



