from sqlalchemy import desc, select, delete, update
from sqlalchemy.exc import NoResultFound

from db.models.posts import Comment, Post
from db.models.user import User
from exceptions.db_exc import NotFoundException, NotOwnerException

async def create_post(db_session, title: str, body: str, author: int):
    new_post = Post(title=title, body=body, author=author)
    db_session.add(new_post)
    await db_session.commit()


async def add_new_comment(db_session, body: str, post_id: int, author: int, comment_id: int | None = None):
    new_comment = Comment(body=body, author=author, post=post_id, parrent_comment_id=comment_id)
    db_session.add(new_comment)
    await db_session.commit()


async def get_post_owner(db_session, post_id: int):
    sql = select(Post.author).where(Post.id == post_id)
    try:
        data = await db_session.execute(sql)
        post = data.one()
    except NoResultFound:
        raise NotFoundException('Post was not found')
    return post

async def get_posts(db_session, page: int):
    sql = select(Post).offset(page * 6).limit(6)
    data = await db_session.execute(sql)
    posts = data.all()
    for en, post in enumerate(posts):
        posts[en] = post[0].__dict__
        posts[en]['author_post'] = post[0].author_post.__dict__
    return posts


async def get_post(db_session, post_id: int):
    try:
        sql = select(Post).where(Post.id == post_id)
        post = await db_session.execute(sql)
        post = post.one()
    except NoResultFound:
        raise NotFoundException('Post was not found')
    post = post[0].__dict__
    post['author_post'] = post['author_post'].__dict__
    return post


async def get_replies(db_session, comment):
    replies = await db_session.execute(comment[0].replies)
    lis = []
    for reply in replies:
        lis.append({
                'comment_id': reply[0].id,
                'body': reply[0].body,
                'likes': reply[0].likes,
                'owner': {
                    'login': comment[0].author_comment.login,
                    'id': comment[0].author_comment.id
                    },
                'replies':await get_replies(db_session, reply),
                'created_on': comment[0].created_on
            })
    return lis if lis else None


async def get_comments(db_session, post_id: int):
    comments_list = []
    topq = select(Comment).filter(Comment.parrent_comment_id == None, Comment.post == post_id).order_by(
            desc(Comment.created_on)
            )
    comments = await db_session.execute(topq)
    comments = comments.unique()
    for comment in comments:
        comments_list.append({
                    'comment_id': comment[0].id,
                    'body': comment[0].body,
                    'likes': comment[0].likes,
                    'owner': {
                        'login': comment[0].author_comment.login,
                        'id': comment[0].author_comment.id
                        },
                    'replies': await get_replies(db_session, comment),
                    'created_on': comment[0].created_on
                })
    return comments_list


async def get_comment_owner(db_session, comment_id: int):
    sql = select(Comment.author).where(Comment.id == comment_id)
    data = await db_session.execute(sql)
    try:
        comment = data.one()
    except NoResultFound:
        raise NotFoundException('Commments was not found')
    return comment


async def update_comment(db_session, comment_id: int, user_id: int, **kwargs):
    comment_owner = await get_comment_owner(db_session, comment_id)
    if comment_owner.author != user_id:
        raise NotOwnerException('comment')
    sql = update(Comment).values(**kwargs).where(Comment.id == comment_id)
    await db_session.execute(sql)
    await db_session.commit()


async def update_post(db_session, post_id: int, user_id: int, **kwargs):
    post_owner = await get_post_owner(db_session, post_id)
    if post_owner.author != user_id:
        raise NotOwnerException
    sql = update(Post).values(**kwargs).where(Post.id == post_id)
    await db_session.execute(sql)
    await db_session.commit()


async def delete_post_by_id(db_session, post_id: int, user_id: int):
    post_owner = await get_post_owner(db_session, post_id)
    if post_owner.author != user_id:
        raise NotOwnerException
    sql = delete(Post).where(Post.id == post_id)
    await db_session.execute(sql)
    await db_session.commit()


async def delete_comment_by_id(db_session, comment_id: int, user_id: int):
    comment_owner = await get_comment_owner(db_session, comment_id)
    if comment_owner.author != user_id:
        raise NotOwnerException
    sql = delete(Comment).where(Comment.id == comment_id)
    await db_session.execute(sql)
    await db_session.commit()
