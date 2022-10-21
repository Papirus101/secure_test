import hashlib

from load_config import password_config, Password

def hash_password_sync(password: str):
    config: Password = password_config()
    enc = hashlib.pbkdf2_hmac(
            config.PASS_ALGORITHM,
            password.encode(),
            config.PASS_SALT.encode(),
            100_000)
    return enc.hex()


async def hash_password(password: str):
    config: Password = password_config()
    enc = hashlib.pbkdf2_hmac(
            config.PASS_ALGORITHM,
            password.encode(),
            config.PASS_SALT.encode(),
            100_000)
    return enc.hex()


async def validate_password(password: str, hashed_password: str):
    return await hash_password(password) == hashed_password

