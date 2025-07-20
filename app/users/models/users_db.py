from datetime import datetime
from typing import Annotated

import bcrypt
from pydantic import AfterValidator
from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy import String, LargeBinary, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from common.config import Base


class Users(Base):
    __tablename__ = "users"

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        password_bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(10), unique=True)
    email: Mapped[str] = mapped_column()
    password: Mapped[bytes] = mapped_column(LargeBinary(60))

    last_publication_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("hash_index_users_email", email, postgresql_using="hash"),
    )

    PasswordType = Annotated[
        str,
        AfterValidator(hash_password),
    ]

    InputSchema = MappedModel.create(
        columns=[
            username,
            email,
            (password, PasswordType)
        ]
    )
    ResponseSchema = MappedModel.create(columns=[id])

    AuthenticateSchema = MappedModel.create(columns=[email, password])

    def is_password_valid(self, password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode("UTF-8"),
            hashed_password=self.password
        )
