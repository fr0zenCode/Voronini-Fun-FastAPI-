from typing import Any

import redis.asyncio as redis

from common.config import settings

REDIS_HOST: str = settings.redis_host
REDIS_PORT: int = settings.redis_port


class RedisController:
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT):
        self._client = redis.Redis(host=host, port=port, decode_responses=True)

    async def close(self):
        await self._client.close()

    async def set(self, key: Any, value: Any):
        try:
            await self._client.set(name=key, value=value)  # TODO: create try - except
        except Exception as e:
            raise RuntimeError(f"Redis | set method | {e}")

    async def get(self, key: Any) -> Any:
        try:
            return await self._client.get(key)
        except Exception as e:
            raise RuntimeError(f"Redis | get method | {e}")

    async def delete(self, key: Any):
        try:
            await self._client.delete(key)
        except Exception as e:
            raise RuntimeError(f"Redis | delete method | {e}")

