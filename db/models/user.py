import os

from sqlalchemy.orm import backref, relationship

from db.base import Base
from sqlalchemy import Boolean, Column, Integer, VARCHAR, event

from depends.auth.password_hash import hash_password_sync


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR, unique=True)
    login = Column(VARCHAR, unique=True)
    password = Column(VARCHAR)
    
    is_admin = Column(Boolean, default=False)

@event.listens_for(User.__table__, 'after_create')
def insert_test_datas_company_types(mapper, connection, *args, **kwargs):
    user = User.__table__
    connection.execute(user.insert().values(
        email=os.getenv('ADMIN_EMAIL'),
        login=os.getenv('ADMIN_USERNAME'),
        password=hash_password_sync(os.getenv('ADMIN_PASSWORD'))))
