import datetime
from datetime import timedelta

import bcrypt
import jwt
from jwt import DecodeError

from database.users.schemas import UserSchema
from app.config import settings
from services.users.errors import UserNotAuthorizedError


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
):
    payload_to_encode = payload.copy()
    now = datetime.datetime.utcnow()
) -> str:
    """
    Создает **JSON Web Token**, в который закодированы переданные функции параметры.

    :param payload: **dict** - словарь с данными, которые должны быть закодированы в JWT;
    :param private_key: **str** - приватный ключ для кодирования. Дефолтное значение - приватный ключ из конфига приложения;
    :param algorithm: **str** - алгоритм шифрования. По дефолту берется из конфига;
    :param expire_minutes: **int** - количество минут, через которые токен сгорит. Дефолтное значение из конфига приложения;
    :param expire_timedelta: **timedelta** - опциональное значение, можно кастомизировать время жизни токена, используя в качестве значения timedelta из библиотеки datetime.

    :return: **str** - encoded JWT
    """

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    print(expire)

    payload_to_encode.update(exp=expire, iat=now)
    encoded_jwt = jwt.encode(payload_to_encode, private_key, algorithm=algorithm)

    return encoded_jwt


def decode_jwt(
        jwt_for_decode: bytes | str,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    """
    **return example** ----> \n
        {
            'email': 'user@example.com', \n
            'exp': 1743545411, \n
            'iat': 1743545111, \n
            'type': 'access', \n
            'user_id': 1, \n
            'username': 'string' \n
        }
    """
    try:
        decoded_jwt = jwt.decode(jwt_for_decode, public_key, algorithms=[algorithm])
        return decoded_jwt
    except DecodeError:
        print("services/auth/core.py/decode_jwt --- Не удалось декодировать JWT.")
        raise UserNotAuthorizedError()


def create_jwt_token(
    token_type: str,
    payload: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
) -> str:
    """
    Создает **JSON Web Token** на основании переданных параметров.

    :param token_type: **str** - тип токена: access или refresh;
    :param payload: **dict** - словарь, в котором хранится информация, которую необходимо закодировать в JWT;
    :param expire_minutes: **int** - количество минут, которые будет жить токен;
    :param expire_timedelta: **datetime.timedelta** - кастомное количество времени, которое будет жить токен;

    :return: **str** - готовый JSON Web Token
    """

    jwt_payload = {"type": token_type}
    jwt_payload.update(payload)

    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )
