"""Utils function for the authentication module."""

import uuid
from datetime import timedelta, datetime, timezone
import logging

from passlib.context import CryptContext
import jwt
from itsdangerous import URLSafeTimedSerializer

from src.config import Config

passwd_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600  # Default in seconds
REFRESH_TOKEN_EXPIRY = 2  # Default in days


def generate_passwd_hash(password: str) -> str:
    """Generates a hash for the password."""
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    """Checks if password provided matches the stored hash."""
    return passwd_context.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
) -> str:
    """Creates a JWT access token with user data."""
    payload = {
        "user": user_data,
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }
    if not refresh:
        payload["exp"] = datetime.now(timezone.utc) + (
            expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
        )
    else:
        payload["exp"] = datetime.now(timezone.utc) + (
            expiry if expiry else timedelta(days=REFRESH_TOKEN_EXPIRY)
        )

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )

    return token


def decode_token(token: str) -> dict:
    """Decodes a JWT access token."""
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
        )

        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


# Serializer for email verification
serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET,
    salt="email-verification",
)


def create_url_safe_token(data: dict):
    """Creates an URL safe token (for account verification, for example)."""
    token = serializer.dumps(data)

    return token


def decode_url_safe_token(token: str):
    """Decodes an URL safe token (for account verification, for example)."""
    try:
        token_data = serializer.loads(token)

        return token_data
    except Exception as e:
        logging.error(str(e))
