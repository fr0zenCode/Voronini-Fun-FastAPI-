import datetime
from typing import Optional, Annotated

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


integer_primary_key = Annotated[int, mapped_column(primary_key=True)]
created_date = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Users(Base):
    __tablename__ = "users"

    id: Mapped[integer_primary_key]

    first_name: Mapped[Optional[str]]
    second_name: Mapped[Optional[str]]
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)


class Publications(Base):
    __tablename__ = "publications"

    id: Mapped[integer_primary_key]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pub_text: Mapped[str]
    created_at: Mapped[created_date]


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"))
    comment_text: Mapped[str]
    created_at: Mapped[created_date]


class Tokens(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    access_token: Mapped[str] = mapped_column(unique=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[integer_primary_key]
