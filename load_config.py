from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')


@dataclass
class DB:
    host: str
    port: str
    user: str
    password: str
    db_name: str


@dataclass
class Auth:
    JWT_ALGORITHM: str
    JWT_SECRET: str


@dataclass
class Password:
    PASS_SALT: str
    PASS_ALGORITHM: str


@dataclass
class Config:
    db: DB
    auth: Auth
    password: Password


def db_config():
    return DB(
            user=getenv('DB_USER'),
            password=getenv('DB_PASS'),
            host=getenv('DB_HOST'),
            port=getenv('DB_PORT'),
            db_name=getenv('DB_NAME')
         )


def auth_config():
    return Auth(
                JWT_SECRET=getenv('JWT_SECRET'),
                JWT_ALGORITHM=getenv('JWT_ALGORITHM')
                )


def password_config():
    return Password(
                PASS_ALGORITHM=getenv('PASSWORD_ALGORITHM'),
                PASS_SALT=getenv('SALT')
                )

