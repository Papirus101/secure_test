from __future__ import annotations
from datetime import datetime

from typing import List
from pydantic import BaseModel

from models.user_model import UserCommentScheme

class CreateCommentScheme(BaseModel):
    body: str
    post_id: int
    comment_id: int | None

class CreatePostScheme(BaseModel):
    title: str
    body: str

class GetPostScheme(BaseModel):
    post_id: int

class PostScheme(CreatePostScheme):
    id: int
    author_post: UserCommentScheme
    likes: int

class ShortPostSheme(BaseModel):
    title: str
    id: int
    author_post: UserCommentScheme
    likes: int

class PostsListSheme(BaseModel):
    posts: List[ShortPostSheme]

class BaseCommentScheme(BaseModel):
    comment_id: int
    body: str
    likes: int
    created_on: datetime
    owner: UserCommentScheme
    replies: List[BaseCommentScheme] | None
    
class ListCommentsScheme(BaseModel):
    comments: List[BaseCommentScheme]

class UpdateCommentScheme(BaseModel):
    comment_id: int
    body: str

class UpdatePostSheme(BaseModel):
    post_id: int
    body: str | None
    title: str | None

