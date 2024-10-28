from pydantic import BaseModel


class UserForRegistrate(BaseModel):
    first_name: str
    second_name: str
    username: str
    email: str
    password: str


class UserForAuthorize(BaseModel):
    email: str
    password: str
