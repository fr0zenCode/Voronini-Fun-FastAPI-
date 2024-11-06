from pydantic import BaseModel


class Post(BaseModel):
    author: str
    text: str
