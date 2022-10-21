from pydantic import BaseModel, EmailStr


class UserBaseScheme(BaseModel):
    email: EmailStr
    login: str

class UserRegisterScheme(UserBaseScheme):
    password: str


class UserCommentScheme(BaseModel):
    id: int
    login: str


class UserLoginScheme(BaseModel):
    login: str
    password: str

class UserUpdateSheme(BaseModel):
    login: str | None
    email: EmailStr | None
    password: str | None


class TokenScheme(BaseModel):
    Authorization: str
