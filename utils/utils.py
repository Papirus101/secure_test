from fastapi import HTTPException, Request
import settings
import aioredis
import os


def get_user_token(request: Request) -> str:
    token = ''
    if settings.AUTH_TYPE == 'data':
        _, token = request.headers.get('Authorization').split()
    elif settings.AUTH_TYPE == 'cookie':
           token = request.cookies.get('Authorization')
           if token is None or len(token) < 1:
               raise HTTPException(403)
           _, token = token.split()
    return token


async def get_redis():
    redis = await aioredis.from_url(f"redis://{os.getenv('REDIS_HOST')}")
    return redis
