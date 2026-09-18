from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from backend.core.config import settings

password_hash = PasswordHash.recommended()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )

    to_encode.update(
        {
            "exp": expire,
        }
    )

    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm="HS256",
    )


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)
