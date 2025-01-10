from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR.parent / "secret_keys" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR.parent / "secret_keys" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def test_database_url_asyncpg(self):
        return (f"postgresql+asyncpg://{self.TEST_DB_USER}:"
                f"{self.TEST_DB_PASS}@"
                f"{self.TEST_DB_HOST}:"
                f"{self.TEST_DB_PORT}/"
                f"{self.TEST_DB_NAME}")

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
