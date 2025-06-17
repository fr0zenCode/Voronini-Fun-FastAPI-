from datetime import datetime

from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from database.core.database import Base


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column()

    header: Mapped[str] = mapped_column(String(100)) # TODO: delete magic number
    text_content: Mapped[str] = mapped_column(String(356)) # TODO: delete magic number

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    __table_args__ = (Index("author_id_hash_index", author_id, postgresql_using="hash"))

    InputSchema = MappedModel.create(columns=[header, text_content])
    PatchSchema = InputSchema.extend(columns=[created_at])
    ResponseSchema = MappedModel.create(columns=[id, author_id, header, text_content, created_at])
