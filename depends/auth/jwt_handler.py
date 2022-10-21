import time
from fastapi import Depends, HTTPException
import json
import jwt
from db.queries.users import get_user_by_login
from db.session import get_session
from load_config import auth_config, Auth
from utils.utils import get_redis, get_user_token


async def token_response(token: str, expires: int) -> dict:
    return {
        'access_token': token,
        'expires': expires
    }


async def signJWT(user_info: str) -> dict:
    config: Auth = auth_config()
    token = jwt.encode(
        {
            'user_info': user_info,
            'expires': int(time.time() + 7200)
        },
        config.JWT_SECRET,
        algorithm=config.JWT_ALGORITHM)
    return await token_response(token, int(time.time() + 7200))


async def decodeJWT(token: str) -> str | None:
    config: Auth = auth_config()
    if isinstance(token, list):
        token = token[0]
    token = token.encode('utf-8')
    decode_token = jwt.decode(token, config.JWT_SECRET, config.JWT_ALGORITHM)
    return decode_token if decode_token['expires'] >= time.time() else None


async def get_login_by_token(token: str = Depends(get_user_token)) -> dict:
    config: Auth = auth_config()
    token = token.encode('utf-8')
    decode_token = jwt.decode(token, config.JWT_SECRET, config.JWT_ALGORITHM)
    if decode_token.get('user_info') is None:
        raise HTTPException(403)
    return {'token': token, 'login': decode_token['user_info']}

async def get_user(db_session = Depends(get_session), user_info: dict = Depends(get_login_by_token), redis = Depends(get_redis)):
    cache = await redis.get(user_info['login'])
    if cache is not None:
        return json.loads(cache)
    user = await get_user_by_login(user_info['login'], db_session)
    user = dict(user)
    del user['password']
    await redis.set(user_info['login'], json.dumps(dict(user)))
    return user
