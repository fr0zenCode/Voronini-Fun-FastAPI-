import uuid

from sqlalchemy import Column, UUID, String, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    ...


class User(Base):

    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())

    first_name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    username = Column(String, nullable=False)

    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

