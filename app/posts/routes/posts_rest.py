import datetime

from fastapi import APIRouter, HTTPException
from starlette import status

from posts.dependencies.posts_dep import PostById
from posts.models.posts import Posts
from users.dependencies.users_dep import GetCurrentAuthorizedUser


post_router = APIRouter(prefix="/posts-api", tags=["Posts API"])


@post_router.post(path="/posts/", summary="Create a post")
async def create_post(post: Posts.InputSchema, user: GetCurrentAuthorizedUser):
    if not user.last_publication_time or (user.last_publication_time + datetime.timedelta(minutes=5) < datetime.datetime.now()):
        user.last_publication_time = datetime.datetime.now()
        return await Posts.create(author_id=user.id, **post.model_dump()) # TODO: типизировать что возвращает
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Посты можно создавать раз в 5 минут, вам осталось подождать еще ...")

@post_router.get(path="/posts/", summary="Get all posts from database", response_model=list[Posts.ResponseSchema])
async def get_all_posts_from_database() -> [Posts]:
    return await Posts.find_all_by_kwargs()

@post_router.get(path="/posts/current-user", summary="Get all current user's posts", response_model=list[Posts.ResponseSchema])
async def get_all_current_user_posts(user: GetCurrentAuthorizedUser) -> [Posts]:
    return await Posts.find_all_by_kwargs(author_id=user.id)

@post_router.get(path="/posts/post/", summary="Get post by id", response_model=Posts.ResponseSchema)
async def get_post_by_id(post: PostById) -> Posts:
    return post

@post_router.delete(path="/post/", status_code=status.HTTP_204_NO_CONTENT, summary="Delete post by id")
async def delete_post_by_id(user: GetCurrentAuthorizedUser, post: PostById):
    if user.id == post.author_id:
        await post.delete()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет прав для удаления этого поста") # todo: alias
