from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from services.auth.auth import AuthService, auth_service_factory

feed_router = APIRouter(prefix="/feed", tags=["feed"])

templates = Jinja2Templates(directory="templates")


# @feed_router.get("/")
# async def get_feed_page(request: Request, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
#     decoded_jwt = await auth_service.is_user_authorized(request=request)
#     return frontend_service.created_feed_template(decoded_jwt=decoded_jwt)
#
#
# @feed_router.get("/load-more-posts")
# async def load_more_posts(offset: int, limit: int):
#     await posts_service.get_more_posts(offset=offset, limit=limit)
#
#
# @feed_router.post("/new-post")
# async def add_new_post(post_for_add: AddPostSchema, request: Request):
#     decoded_jwt = await auth_service.is_user_authorized(request=request)
#     await posts_service.add_post(decoded_jwt=decoded_jwt, post_for_add=post_for_add)
#
#
# @feed_router.post("/delete-post")
# async def delete_post(post_id: int, request: Request):
#     decoded_jwt = await auth_service.is_user_authorized(request=request)
#     await posts_service.delete_post(post_id=post_id)
