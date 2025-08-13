from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from posts.models.posts import Posts
from users.aliases import POST_ID_NON_EXIST_ALIAS


async def get_post_by_id(post_id: int) -> Posts:
    post = await Posts.find_first_by_id(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=POST_ID_NON_EXIST_ALIAS)
    return post

PostById = Annotated[Posts, Depends(get_post_by_id)]
