import datetime

import jwt
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from jwt import ExpiredSignatureError
from starlette.responses import RedirectResponse

from auth.utils import check_cookie, decode_jwt
from config import settings
from db.schemas import Post
from modules.post.schemas import PostInfo, PostForDelete
from modules.post.crud import post_crud
from sqlalchemy.exc import InterfaceError

feed_router = APIRouter(prefix="/feed", tags=["feed"])

templates = Jinja2Templates(directory="templates")


@feed_router.get("/")
async def get_feed_page(request: Request, jwt_token: str = Depends(check_cookie)):
    try:
        decoded_jwt = decode_jwt(
                token=jwt_token,
                public_key=settings.auth_jwt.public_key_path.read_text(),
                algorithm=settings.auth_jwt.algorithm
            )
        context = {
            "posts": await post_crud.get_more_posts(offset=0, limit=10),
            "current_user_id": decoded_jwt["sub"]
        }
        return templates.TemplateResponse(request, "feed.html", context=context)
    except ExpiredSignatureError:
        print(request.client)
        print(jwt_token)
        print("Срок действия токена истёк")
        return RedirectResponse("/user/login", status_code=302)


@feed_router.get("/load-more-posts")
async def load_more_posts(offset: int, limit: int):

    posts = await post_crud.get_more_posts(offset=offset, limit=limit)

    posts = [{
        "post_id": post.post_id,
        "author_username": post.author_username,
        "author_id": post.author_id,
        "created_at": post.created_at.isoformat(),
        "text": post.text
    } for post in posts]

    print(f"offset: {offset}")
    return {"posts": posts}


@feed_router.post("/comment")
def add_comment(jwt_token=Depends(check_cookie)):
    print(f"From add_comment function: {jwt_token}")


@feed_router.post("/new-post")
async def add_new_post(post: Post, jwt_token=Depends(check_cookie)):

    if post.text:

        decoded_jwt = jwt.decode(
            jwt_token,
            key=settings.auth_jwt.public_key_path.read_text(),
            algorithms=[settings.auth_jwt.algorithm]
        )

        new_post = PostInfo(
            author_username=decoded_jwt["username"],
            author_id=decoded_jwt["sub"],
            text=post.text,
            created_at=datetime.datetime.utcnow()
        )

        return await post_crud.add_post(new_post)
    else:
        return {"message": "failed",
                "detail": "empty post"}


@feed_router.post("/delete-post")
async def delete_post(post_for_delete: PostForDelete):
    try:
        await post_crud.delete_post_by_id(post_for_delete.post_id)
        return {"message": "successful"}
    except InterfaceError as db_err:
        return {"message": "failed",
                "details": db_err}
