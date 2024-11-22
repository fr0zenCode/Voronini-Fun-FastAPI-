import datetime

import jwt
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.responses import RedirectResponse, Response, JSONResponse

import auth
from auth.utils import check_cookie, decode_jwt
from config import settings
from db.schemas import Post
from modules.post.schemas import PostInfo, PostForDelete
from modules.post.crud import post_crud
from sqlalchemy.exc import InterfaceError

from modules.user.crud import user_crud

feed_router = APIRouter(prefix="/feed", tags=["feed"])

templates = Jinja2Templates(directory="templates")


def redirect_to_login_page_and_delete_cookies(login_page_url="/user/login"):
    response = RedirectResponse(url=login_page_url)
    response.delete_cookie("jwt")
    response.delete_cookie("jwt_refresh_token")
    return response


@feed_router.get("/")
async def get_feed_page(request: Request):

    check_cookies_result = await auth.utils.check_cookie(request=request)

    if check_cookies_result == "FALSE":
        return redirect_to_login_page_and_delete_cookies()

    access_token = ""

    if check_cookies_result == "TRUE":
        access_token = request.cookies.get("jwt")

    if not access_token:
        access_token = check_cookies_result

    decoded_jwt = jwt.decode(
        jwt=access_token,
        key=settings.auth_jwt.public_key_path.read_text(),
        algorithms=[settings.auth_jwt.algorithm]
    )

    context = {
        "posts": await post_crud.get_more_posts(offset=0, limit=10),
        "current_user_id": decoded_jwt["sub"]
    }

    response = templates.TemplateResponse(request, "feed.html", context=context)
    response.set_cookie("jwt", access_token)
    return response


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


class Post(BaseModel):
    author: str
    text: str


@feed_router.post("/new-post")
async def add_new_post(post: Post, request: Request, response: Response):

    jwt_token = request.cookies.get("jwt")

    res = await auth.utils.check_cookie(request=request)

    if res == "FALSE":
        return redirect_to_login_page_and_delete_cookies()

    elif res == "TRUE":
        ...

    else:
        jwt_token = res

    response.set_cookie("jwt", jwt_token)
    decoded_jwt = decode_jwt(jwt_token)

    if post.text:
        new_post = PostInfo(
            author_username=decoded_jwt["username"],
            author_id=decoded_jwt["sub"],
            text=post.text,
            created_at=datetime.datetime.utcnow().replace(microsecond=0)
        )

        last_pub_time = await user_crud.get_last_publication_time_by_id(decoded_jwt["sub"])

        if last_pub_time is None or datetime.datetime.utcnow() - last_pub_time > datetime.timedelta(minutes=5):
            await post_crud.add_post(new_post)
            await user_crud.set_last_publication_time(user_id=decoded_jwt["sub"], time=datetime.datetime.utcnow())
            return {"message": "successful",
                    "detail": "new post created"}
        else:
            return JSONResponse(content={"message": "successful", "detail": "слишком много постов"}, status_code=400)
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
