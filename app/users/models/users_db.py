import re
from datetime import datetime
from typing import Annotated

import bcrypt
from email_validator import validate_email
from pydantic import AfterValidator
from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy import LargeBinary, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column
from fastapi import HTTPException

from common.config import Base
from users.aliases import USERNAME_VALIDATION_REGEXP, INVALID_USERNAME, INVALID_EMAIL, ENCODING_TYPE


class Users(Base):
    __tablename__ = "users"

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        password_bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)

    @staticmethod
    def validate_email_custom(email: str) -> str:
        try:
            validate_email(email, check_deliverability=False) # TODO: в прод мод надо будет проверку на домены поставить
        except Exception as e:
            print(e) # TODO: log
            raise HTTPException(status_code=400, detail=INVALID_EMAIL)
        return email

    @staticmethod
    def validate_username(username: str) -> str:
        if re.match(USERNAME_VALIDATION_REGEXP, username):
            return username
        raise HTTPException(status_code=400, detail=INVALID_USERNAME)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[bytes] = mapped_column(LargeBinary(60))

    last_publication_time: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=True)

    __table_args__ = (
        Index("hash_index_users_email", email, postgresql_using="hash"),
    )

    PasswordType = Annotated[
        str,
        AfterValidator(hash_password),
    ]

    EmailType = Annotated[
        str,
        AfterValidator(validate_email_custom)
    ]

    UsernameType = Annotated[
        str,
        AfterValidator(validate_username)
    ]

    InputSchema = MappedModel.create(
        columns=[
            (username, UsernameType),
            (email, EmailType),
            (password, PasswordType)
        ]
    )
    ResponseSchema = MappedModel.create(columns=[id, username, email])
    EmailSchema = MappedModel.create(columns=[email])
    UsernameSchema = MappedModel.create(columns=[username])
    AuthenticateSchema = MappedModel.create(columns=[email, password])

    def is_password_valid(self, password: str) -> bool:
        return bcrypt.checkpw(
            password=str(password).encode(ENCODING_TYPE),
            hashed_password=self.password
        )
