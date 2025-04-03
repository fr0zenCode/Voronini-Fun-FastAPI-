from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.requests import Request

from api.posts import post_router
from api.user import user_router

from database.errors import DatabaseLoseConnection, DatabaseTablesErrors, UserWithTheSameUsernameIsAlreadyExistsError, \
    UserWithTheSameEmailIsAlreadyExistsError, DatabaseColumnsErrors
from services.users.errors import IncorrectCredentialsError, UserNotAuthorizedError

BASE_DIR = Path(__file__).parent
static_folder = "static"


app = FastAPI()


@app.exception_handler(DatabaseLoseConnection)
async def database_lose_connection_errors_handler(request: Request, exception: DatabaseLoseConnection):
    raise HTTPException(
        status_code=503,
        detail=exception.message
    )


@app.exception_handler(DatabaseTablesErrors)
async def database_tables_errors_handler(request: Request, exception: DatabaseTablesErrors):
    raise HTTPException(
        status_code=503,
        detail=exception.message
    )


@app.exception_handler(UserWithTheSameUsernameIsAlreadyExistsError)
async def user_with_the_same_username_is_already_exists_error_handler(
        request: Request, exception: DatabaseTablesErrors
):
    raise HTTPException(
        status_code=409,
        detail=exception.message
    )


@app.exception_handler(UserWithTheSameEmailIsAlreadyExistsError)
async def user_with_the_same_email_is_already_exists_error_handler(request: Request, exception: DatabaseTablesErrors):
    raise HTTPException(
        status_code=409,
        detail=exception.message
    )


@app.exception_handler(DatabaseColumnsErrors)
async def database_columns_errors_handler(request: Request, exception: DatabaseTablesErrors):
    raise HTTPException(
        status_code=409,
        detail=exception.message
    )


@app.exception_handler(IncorrectCredentialsError)
async def incorrect_user_credentials_for_login_error_handler(request: Request, exception: IncorrectCredentialsError):
    raise HTTPException(
        status_code=401,
        detail=exception.message
    )


@app.exception_handler(UserNotAuthorizedError)
async def user_not_authorized_error_handler(request: Request, exception: UserNotAuthorizedError):
    raise HTTPException(
        status_code=401,
        detail=exception.message
    )


app.include_router(user_router)
app.include_router(post_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
