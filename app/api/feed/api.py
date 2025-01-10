from typing import Annotated

from fastapi import APIRouter, Depends

from database.posts.schemas import PostSchema
from services.feed.abstract import AbstractFeedService
from services.feed.feed import feed_service_factory

feed_router = APIRouter(prefix="/feed", tags=["Feed API"])


@feed_router.get("/get-posts-portion")
async def get_posts_portion(
        feed_service: Annotated[AbstractFeedService, Depends(feed_service_factory)],
        limit: int = 10,
        offset: int = 0
) -> list[PostSchema]:
    posts = await feed_service.get_posts_portion(limit=limit, offset=offset)
    return posts
