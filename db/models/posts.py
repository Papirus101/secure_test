from sqlalchemy.orm import backref, relationship
from db.base import Base
from sqlalchemy import Column, DateTime, Integer, VARCHAR, ForeignKey, func




class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(VARCHAR)
    created_on = Column(DateTime, server_default=func.now())
    post = Column(ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    parrent_comment_id = Column(ForeignKey('comments.id', ondelete='CASCADE'), nullable=True)
    author = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    likes = Column(Integer, default=0, nullable=False)

    replies = relationship('Comment', backref=backref('parent', remote_side=[id]), lazy='dynamic')
    author_comment = relationship('User', backref=backref('owner_comment'), lazy='joined')
    # post = relationship('Post', backref=backref('comments'))

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR)
    body = Column(VARCHAR)
    likes = Column(Integer, default=0)
    author = Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    author_post = relationship('User', backref=backref('owner_post'), lazy='joined')

