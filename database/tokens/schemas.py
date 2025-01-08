from pydantic import BaseModel


class TokenSchema(BaseModel):
    user_id: int
    refresh_token: str
