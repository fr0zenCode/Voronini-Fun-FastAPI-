import datetime

from pydantic import BaseModel


class PostInfo(BaseModel):

    author_username: str
    author_id: str

    text: str
    created_at: datetime.datetime


class PostFromDB(PostInfo):
    post_id: int


class PostForDelete(BaseModel):
    post_id: int
