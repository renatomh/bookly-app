"""Dependencies for the authentication module."""

from typing import List

from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .utils import decode_token
from .service import UserService
from src.db.models import User
from src.db.redis import token_in_blocklist
from src.db.main import get_session

user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        creds = await super().__call__(request)

        token = creds.credentials

        if not self.is_token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired.",
                    "resolution": "Please get a new token.",
                },
            )

        token_data = decode_token(token)

        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or has been revoked.",
                    "resolution": "Please get a new token.",
                },
            )

        self.verify_token_data(token_data)

        return token_data

    def is_token_valid(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Please override this method in child classes.")


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token.",
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token.",
            )


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    """Get data for the current user."""
    user_email = token_details["user"]["email"]

    # NOTE: we should try to implement cache for this
    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:

    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:
        # NOTE: we might not even need to query the user, since the 'role' is now included in the token details
        # TODO: check if we can access 'token_details' here
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action.",
        )
