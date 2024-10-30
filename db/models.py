import datetime

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    first_name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    username = Column(String, nullable=False)

    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class Publications(Base):

    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class Comments(Base):

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id"), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
