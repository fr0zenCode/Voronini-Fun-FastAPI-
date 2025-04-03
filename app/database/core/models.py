import datetime
from typing import Annotated

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..core.database import Base
from database.repositories.tokens.schemas import TokenSchema
from ..repositories.posts.schemas import PostSchema
from ..repositories.users.schemas import UserSchema

created_time = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Users(Base):

    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str]
    second_name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    is_active: Mapped[bool]
    last_publication_time: Mapped[datetime.datetime] = mapped_column(nullable=True)

    def convert_to_pydantic_model(self):
        return UserSchema(
            id=self.id,
            first_name=self.first_name,
            second_name=self.second_name,
            username=self.username,
            email=self.email,
            password=self.password.decode("utf-8"),
            last_publication_time=self.last_publication_time
        )


class Posts(Base):

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_username: Mapped[str]
    text_content: Mapped[str]
    created_at: Mapped[created_time]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def convert_to_pydantic_model(self):
        return PostSchema(
            id=self.id,
            author_id=self.author_id,
            author_username=self.author_username,
            text_content=self.text_content,
            created_at=self.created_at
        )


class Tokens(Base):

    __tablename__ = "tokens"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)

    def convert_to_pydantic_model(self):
        return TokenSchema(
            user_id=self.user_id,
            refresh_token=self.refresh_token
        )
