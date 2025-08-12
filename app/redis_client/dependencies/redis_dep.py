from typing import Annotated

from fastapi import Request, Depends

from redis_client.redis_controller import RedisController


async def get_redis_controller_from_request(request: Request) -> RedisController:
    return request.app.state.redis_controller


GetRedisController = Annotated[RedisController, Depends(get_redis_controller_from_request)]
