from fastapi import APIRouter
from starlette import status

from users.dependencies.users_dep import GetCurrentAuthorizedUser
from users.models.users_db import Users


user_router = APIRouter(prefix="/users", tags=["User"])

@user_router.post(
    path="/user/",
    status_code=status.HTTP_201_CREATED,
    response_model=Users.ResponseSchema,
    summary="Create a new user"
)
async def create_user(user_data: Users.InputSchema) -> Users:
    return await Users.create(**user_data.model_dump())


@user_router.get(
    path="/user/",
    summary="Get current authenticated user"
)
async def get_current_user(user: GetCurrentAuthorizedUser):
    return user
