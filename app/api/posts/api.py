import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response

from database.posts.schemas import AddPostSchema, AddFromFastAPIPostSchema, PostSchema
from services.auth.auth import auth_service_factory, AuthService
from services.posts.posts import AbstractPostsService, posts_service_factory

post_router = APIRouter(prefix="/posts", tags=["Posts API"])


@post_router.post("/add-post")
async def add_post(
        request: Request,
        response: Response,
        auth_service: Annotated[AuthService, Depends(auth_service_factory)],
        posts_service: Annotated[AbstractPostsService, Depends(posts_service_factory)],
        post: AddFromFastAPIPostSchema
) -> PostSchema:
    access_token = await auth_service.is_user_authorized(access_token=request.cookies.get("access-token"),
                                                         refresh_token=request.cookies.get("refresh-token"))

    response.set_cookie(key=auth_service.ACCESS_TOKEN_COOKIES_ALIAS, value=access_token)
    user_info = await auth_service.convert_jwt_to_read_format(jwt=access_token)

    add_post_schema = AddPostSchema(
        author_username=user_info["username"],
        author_id=user_info["id"],
        created_at=datetime.datetime.utcnow(),
        text_content=post.text_content
    )

    new_post_id = await posts_service.add_post(post=add_post_schema)
    new_post = await posts_service.get_post_by_id(post_id=new_post_id)

    return new_post


@post_router.post("/delete-post-by-id")
async def delete_post_by_id(
        post_id: int,
        request: Request,
        response: Response,
        auth_service: Annotated[AuthService, Depends(auth_service_factory)],
        posts_service: Annotated[AbstractPostsService, Depends(posts_service_factory)]
) -> dict:
    access_token = await auth_service.is_user_authorized(access_token=request.cookies.get("access-token"),
                                                         refresh_token=request.cookies.get("refresh-token"))

    response.set_cookie(key=auth_service.ACCESS_TOKEN_COOKIES_ALIAS, value=access_token)
    await posts_service.delete_post(post_id=post_id)
    return {"message": f"post with id {post_id} successfully deleted."}


@post_router.get("/get-post-by-id")
async def get_post_by_id(
        post_id: int,
        posts_service: Annotated[AbstractPostsService, Depends(posts_service_factory)]
) -> PostSchema:
    post = await posts_service.get_post_by_id(post_id=post_id)
    return post


@post_router.get("/get-all-posts")
async def get_all_posts(
        posts_service: Annotated[AbstractPostsService, Depends(posts_service_factory)]
) -> list[PostSchema]:
    posts = await posts_service.get_all_posts()
    return posts
