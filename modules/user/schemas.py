from pydantic import BaseModel, EmailStr


class UserForRegistrate(BaseModel):
    first_name: str
    second_name: str
    first_name: str | None = None
    second_name: str | None = None
    username: str
    email: EmailStr
    password: str


class UserForLogin(BaseModel):
    email: str
    password: str
