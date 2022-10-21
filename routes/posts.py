from db.queries.posts import add_new_comment, create_post, delete_comment_by_id, delete_post_by_id, get_comments, get_post, get_posts, update_comment, update_post
from db.queries.users import get_user_by_login
from models.post_model import CreateCommentScheme, CreatePostScheme, ListCommentsScheme, PostScheme, PostsListSheme, UpdateCommentScheme, UpdatePostSheme

from fastapi import APIRouter, Response, Body, Depends

from depends.auth.jwt_bearer import OAuth2PasswordBearerCookie
from depends.auth.jwt_handler import get_login_by_token, get_user
from db.session import get_session

posts_router = APIRouter(
        prefix='/posts',
        tags=['posts']
        )


@posts_router.post('/create_post', status_code=201, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def create_new_post(post: CreatePostScheme = Body(),
        db_session = Depends(get_session), user: dict = Depends(get_user)):
    await create_post(db_session, author=user['id'],  **post.__dict__)
    return Response(status_code=201)


@posts_router.post('/new_comment', status_code=201, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def create_new_comment(comment: CreateCommentScheme = Body(),
        db_session = Depends(get_session), user: dict = Depends(get_user)):
    await add_new_comment(db_session, author=user['id'], **comment.__dict__)


@posts_router.get('/get_comments', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())],
        response_model=ListCommentsScheme)
async def comments(post_id: int, db_session = Depends(get_session)):
    data = await get_comments(db_session, post_id)
    return {'comments': data}


@posts_router.get('/get_posts', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())],
        response_model=PostsListSheme)
async def get_posts_list(page: int = 0, db_session = Depends(get_session)):
    posts = await get_posts(db_session, page)
    return {'posts': posts}

@posts_router.get('/get_post', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())],
        response_model=PostScheme)
async def post(post_id: int, db_session = Depends(get_session)):
        data = await get_post(db_session, post_id)
        return data

@posts_router.patch('/update_comment', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def edit_comment(db_session = Depends(get_session),
        comment_params: UpdateCommentScheme = Body(), user: dict = Depends(get_user)):
    params = {k: v for k, v in comment_params.__dict__.items() if v is not None}
    comment_id = params.pop('comment_id')
    await update_comment(db_session, comment_id, user['id'], **params)


@posts_router.patch('/update_post', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def edit_post(db_session = Depends(get_session), post_params: UpdatePostSheme = Body(),
        user: dict = Depends(get_user)):
    params = {k: v for k, v in post_params.__dict__.items() if v is not None}
    post_id = params.pop('post_id')
    await update_post(db_session, post_id=post_id, user_id=user['id'], **params)


@posts_router.delete('/delete_post', status_code=204, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def delete_post(post_id: int, db_session = Depends(get_session), user: dict = Depends(get_user)):
    await delete_post_by_id(db_session, post_id, user['id'])


@posts_router.delete('/delete_comment', status_code=204, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def delete_comment(comment_id: int, db_session = Depends(get_session), user: dict = Depends(get_user)):
    await delete_comment_by_id(db_session, comment_id, user['id'])
