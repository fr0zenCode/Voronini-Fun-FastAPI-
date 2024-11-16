import datetime
from typing import Optional, Annotated

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base

created_date = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Users(Base):
    __tablename__: str = "users"

    user_id: Mapped[str] = mapped_column(primary_key=True)

    first_name: Mapped[Optional[str]]
    second_name: Mapped[Optional[str]]
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=True)


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_username: Mapped[str]
    text: Mapped[str]
    created_at: Mapped[created_date]

    author_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str]
    created_at: Mapped[created_date]


class Tokens(Base):
    __tablename__ = "tokens"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)
