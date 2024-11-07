from pydantic import BaseModel, EmailStr


class UserForRegistrate(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
    username: str
    email: EmailStr
    password: str


class UserRepresentation(BaseModel):
    user_id: str
    first_name: str
    second_name: str
    username: str
    email: EmailStr
    password: bytes


class UserForLogin(BaseModel):
    email: str
    password: str


class UserLite(BaseModel):
    user_id: str
    username: str
    email: str
