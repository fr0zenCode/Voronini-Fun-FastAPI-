from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "secret_keys" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "secret_keys" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
