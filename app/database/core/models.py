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


class Tokens(Base):

    __tablename__ = "tokens"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)

    def convert_to_pydantic_model(self):
        return TokenSchema(
            user_id=self.user_id,
            refresh_token=self.refresh_token
        )
