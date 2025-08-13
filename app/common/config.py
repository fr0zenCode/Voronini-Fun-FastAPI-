from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from common.sqlalchemy_ext import MappingBase


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_pass: str
    postgres_name: str

    redis_host: str
    redis_port: int

    production_mode: bool = False

    @computed_field
    @property
    def postgres_dsn(self) -> str:
        return (
            "postgresql+psycopg://"
            f"{self.postgres_user}"
            f":{self.postgres_pass}"
            f"@{self.postgres_host}"
            f"/{self.postgres_name}"
        )

settings = Settings()

engine = create_async_engine(settings.postgres_dsn)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase, MappingBase):
    __tablename__: str
    __abstract__: bool
