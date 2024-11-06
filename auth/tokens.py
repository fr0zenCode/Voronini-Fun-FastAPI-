from datetime import timedelta

import auth.utils
from config import settings


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt_token(
        token_type: str,
        payload: dict,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(payload)
    return auth.utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
    )


def create_access_token(user):
    jwt_payload = {
        "sub": user["user_id"],
        "username": user["username"],
        "email": user["email"]
    }
    access_token = create_jwt_token(
        token_type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload
    )
    return access_token


def create_refresh_token(user):
    jwt_payload = {"sub": user["user_id"]}
    refresh_token = create_jwt_token(
        token_type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days)
    )
    return refresh_token
