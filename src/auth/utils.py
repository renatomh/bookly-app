"""Utils function for the authentication module."""

from passlib.context import CryptContext

passwd_context = CryptContext(schemes=["bcrypt"])


def generate_passwd_hash(password: str) -> str:
    """Generates a hash for the password."""
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    """Checks if password provided matches the stored hash."""
    return passwd_context.verify(password, hash)
