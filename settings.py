# DB SETTINGS
ASYNC_DB_LINK="postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
SYNC_DB_LINK="postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# AUTH SETTINGS 'cookie' or 'data'
AUTH_TYPE='cookie'

USER_PHOTO_PATH='images/avatar/{user_login}.{ext}'
