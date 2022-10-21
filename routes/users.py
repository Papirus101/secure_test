import settings
import json
import aiofiles

from fastapi import APIRouter, Response, HTTPException, Body, Depends, UploadFile
from db.queries.users import get_user_by_login, insert_new_client, update_user_data

from depends.auth.jwt_bearer import OAuth2PasswordBearerCookie
from depends.auth.password_hash import hash_password, validate_password
from depends.auth.jwt_handler import get_user, signJWT, get_login_by_token
from db.session import get_session
from models.user_model import TokenScheme, UserLoginScheme, UserRegisterScheme, UserUpdateSheme
from utils.utils import get_redis

users_router = APIRouter(
        prefix='/user',
        tags=['users']
        )

@users_router.post('/create_user', status_code=201, response_model=TokenScheme)
async def user_signup(response: Response, user: UserRegisterScheme = Body(),
        session = Depends(get_session)):
    user.password = await hash_password(user.password)
    new_user = await insert_new_client(session, **user.__dict__)
    if new_user is not None and 'error' in new_user:
        raise HTTPException(400, new_user)
    token = await signJWT(user.login)
    if settings.AUTH_TYPE == 'cookie':
        response.set_cookie('Authorization', f"Bearer {token['access_token']}")
    return {'Authorization': f"Bearer {token['access_token']}"}


@users_router.post('/login', status_code=200, response_model=TokenScheme)
async def user_login(response: Response, user: UserLoginScheme = Body(),
        db_session = Depends(get_session)):
    user_db = await get_user_by_login(user.login, db_session)
    if not await validate_password(user.password, user_db.password):
        raise HTTPException(400, 'Login or password is not valid')
    token = await signJWT(user.login)
    if settings.AUTH_TYPE == 'cookie':
        response.set_cookie('Authorization', f"Bearer {token['access_token']}")
    return {'Authorization': f"Bearer {token['access_token']}"}


@users_router.patch('/update_user', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def user_update_data(response: Response, user: UserUpdateSheme = Body(),
        db_session = Depends(get_session), redis = Depends(get_redis),
        user_info: dict = Depends(get_login_by_token)):
    user_update_data = {k:v for k, v in user.__dict__.items() if v is not None}
    if 'password' in user_update_data:
        user_update_data['password'] = await hash_password(user_update_data['password'])
    await update_user_data(db_session, user_info['login'], **user_update_data)
    await redis.delete(user_info['login'])
    if 'login' in user_update_data:
        user_token = await signJWT(user_update_data['login'])
        user_token = user_token['access_token']
        if settings.AUTH_TYPE == 'cookie':
            response.set_cookie('Authorization', f"Bearer {user_token}")
    return {'Authorization': f"Bearer {user_info['token']}"}


@users_router.post('/update_user_photo', status_code=204, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def update_user_photo(photo: UploadFile, user_info: dict = Depends(get_login_by_token)):
    if photo.content_type.find("image") == -1:
        raise HTTPException(404, "not valid photo")
    ext = photo.filename.split('.')[-1]
    user_login = user_info['login']
    file_path = settings.USER_PHOTO_PATH.format(user_login=user_login.lower(), ext=ext)
    async with aiofiles.open(file_path, "wb") as out_file:
        photo_content = await photo.read()
        await out_file.write(photo_content)


@users_router.get('/get_user', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def get_user_info(user: dict = Depends(get_user)):
    return user

@users_router.get('/logout', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def logout_user(response: Response):
    if settings.AUTH_TYPE == 'cookie':
        response.delete_cookie('Authorization')
    return {'bye': 'bye'}
