from datetime import datetime

from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from database.core.database import Base
from common.config import Base

POST_HEADER_MAX_LENGTH = 100
POST_TEXT_CONTENT_MAX_LENGTH = 356


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column()

    header: Mapped[str] = mapped_column(String(100)) # TODO: delete magic number
    text_content: Mapped[str] = mapped_column(String(356)) # TODO: delete magic number

    header: Mapped[str] = mapped_column(String(POST_HEADER_MAX_LENGTH))
    text_content: Mapped[str] = mapped_column(String(POST_TEXT_CONTENT_MAX_LENGTH))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    __table_args__ = (Index("author_id_hash_index", author_id, postgresql_using="hash"), )

    InputSchema = MappedModel.create(columns=[header, text_content])
    PatchSchema = InputSchema.extend(columns=[created_at]).as_patch()
    ResponseSchema = InputSchema.extend(columns=[id, author_id, created_at])
