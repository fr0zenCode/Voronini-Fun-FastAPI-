from fastapi import APIRouter
from starlette import status

from users.dependencies.users_dep import GetCurrentAuthorizedUser
from users.models.users_db import Users
from users.utils.users_utils import create_user_util

user_router = APIRouter(prefix="/users-api", tags=["User"])

@user_router.post(
    path="/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=Users.ResponseSchema,
    summary="Create a new user"
)
async def create_user(user_data: Users.InputSchema) -> Users:
    return await create_user_util(user_data)


@user_router.get(
    path="/users/user/",
    summary="Get current authenticated user"
)
async def get_current_user(user: GetCurrentAuthorizedUser):
    return user
