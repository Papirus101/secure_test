from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from db.models.user import User
from exceptions.db_exc import FieldAlredyExist, NotFoundException


async def insert_new_client(db_session, **kwargs):
    new_client = User(**kwargs)
    try:
        db_session.add(new_client)
        await db_session.commit()
    except IntegrityError:
        raise FieldAlredyExist


async def get_user_by_login(user_login: str, db_session):
    sql = select(User.id, User.login, User.email, User.password).where(User.login == user_login)
    try:
        data = await db_session.execute(sql)
        data = data.one()
    except NoResultFound:
        raise NotFoundException
    return data


async def update_user_data(db_session, user_login: str, **kwargs):
    sql = update(User).where(User.login == user_login).values(**kwargs)
    try:
        await db_session.execute(sql)
        await db_session.commit()
    except IntegrityError:
        raise FieldAlredyExist

async def delete_user(db_session, user_login: str):
    sql = delete(User).where(User.login == user_login)
    await db_session.execute(sql)
    await db_session.commit()
