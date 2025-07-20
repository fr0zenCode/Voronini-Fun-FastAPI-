from typing import Annotated

from fastapi import Depends
from starlette import status

from posts.models.posts import Posts


async def get_post_by_id(post_id: int) -> Posts:
    post = await Posts.find_first_by_id(post_id)
    if not post:
        raise status.HTTP_404_NOT_FOUND
    return post

PostById = Annotated[Posts, Depends(get_post_by_id)]
