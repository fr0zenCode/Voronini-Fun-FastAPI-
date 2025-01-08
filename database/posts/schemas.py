from datetime import datetime

from pydantic import BaseModel


class AddPostSchema(BaseModel):
    author_username: str
    author_id: int
    text_content: str
    created_at: datetime


class PostSchema(BaseModel):
    id: int
    author_username: str
    author_id: int
    text_content: str
    created_at: datetime
