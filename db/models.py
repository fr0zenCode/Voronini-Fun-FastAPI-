import datetime
from typing import Optional, Annotated

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base

created_date = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(primary_key=True)

    first_name: Mapped[Optional[str]]
    second_name: Mapped[Optional[str]]
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=True)


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str]
    created_at: Mapped[created_date]


class Tokens(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    access_token: Mapped[str] = mapped_column(unique=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[integer_primary_key]
