from typing import Final, Annotated
from datetime import datetime

from pydantic import AfterValidator
from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column
from fastapi import HTTPException
from starlette import status

from common.config import Base
from users.aliases import TOO_LONG_TEXT_ALIAS


POST_HEADER_MAX_LENGTH: Final[int] = 100
POST_TEXT_CONTENT_MAX_LENGTH: Final[int] = 356


class Posts(Base):
    __tablename__ = "posts"

    @staticmethod
    def validate_header(header: str) -> str:
        if len(header) > POST_HEADER_MAX_LENGTH:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=TOO_LONG_TEXT_ALIAS)
        return header

    @staticmethod
    def validate_post_text(post_text: str) -> str:
        if len(post_text) > POST_TEXT_CONTENT_MAX_LENGTH:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=TOO_LONG_TEXT_ALIAS)
        return post_text

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column()

    header: Mapped[str] = mapped_column(String(POST_HEADER_MAX_LENGTH))
    text_content: Mapped[str] = mapped_column(String(POST_TEXT_CONTENT_MAX_LENGTH))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    __table_args__ = (Index("author_id_hash_index", author_id, postgresql_using="hash"), )

    HeaderType = Annotated[
        str,
        AfterValidator(validate_header)
    ]

    PostTextType = Annotated[
        str,
        AfterValidator(validate_post_text)
    ]

    InputSchema = MappedModel.create(
        columns=[
            (header, HeaderType),
            (text_content, PostTextType)
        ]
    )

    PatchSchema = InputSchema.extend(columns=[created_at]).as_patch()
    ResponseSchema = InputSchema.extend(columns=[id, author_id, created_at])
