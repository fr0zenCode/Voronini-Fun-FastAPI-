import datetime

from pydantic import BaseModel, EmailStr


class UserAddSchema(BaseModel):
    first_name: str
    second_name: str
    username: str
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: int
    first_name: str
    second_name: str
    username: str
    email: EmailStr
    password: str
    last_publication_time: datetime.datetime | None


class UsersCredentialsForLogin(BaseModel):
    email: EmailStr
    password: str
