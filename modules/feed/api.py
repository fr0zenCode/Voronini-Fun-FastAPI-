import datetime

import jwt
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from auth.utils import check_cookie
from config import settings
from db.orm import AsyncORM
from db.schemas import Post

BASE_DIR = Path(__file__).parent.parent.parent
static_folder = "static"


feed_router = APIRouter(prefix="/feed", tags=["feed"])

templates = Jinja2Templates(directory="templates")


@feed_router.get("/")
async def get_feed_page(request: Request, jwt_token: str = Depends(check_cookie)) -> templates.TemplateResponse:
    print('hello world')
    posts_from_db = await AsyncORM.get_posts()
    print(jwt_token)
    posts = [Post(author=post[1], text=post[2]) for post in posts_from_db]

    context = {"posts": posts}
    return templates.TemplateResponse(request=request, name="feed.html", context=context)


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
