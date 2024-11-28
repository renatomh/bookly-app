"""
Routes for the authentication module.
"""

from datetime import datetime

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_limiter.depends import RateLimiter

from .schemas import (
    UserModel,
    UserCreateModel,
    UserLoginModel,
    UserLoginResponseModel,
    UserBooksModel,
    RefreshTokenResponseModel,
    RevokeTokenResponseModel,
)
from .service import UserService
from .utils import create_access_token, verify_password
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    RoleChecker,
    get_current_user,
)
from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken

auth_router = APIRouter()
user_service = UserService()
refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()
# This will define routes allowed only for specified user roles
role_checker = RoleChecker(["admin", "user"])


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    """Creates a new user account."""
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post(
    "/login",
    response_model=UserLoginResponseModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RateLimiter(times=2, seconds=10))],
)
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    """Allows an user to login."""
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if not user:
        raise InvalidCredentials()

    password_valid = verify_password(password, user.password_hash)

    if not password_valid:
        raise InvalidCredentials()

    access_token = create_access_token(
        user_data={
            "email": user.email,
            "user_uid": str(user.uid),
            "role": user.role,
        }
    )

    refresh_token = create_access_token(
        user_data={
            "email": user.email,
            "user_uid": str(user.uid),
        },
        refresh=True,
    )

    return JSONResponse(
        content={
            "message": "Login successful.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "uid": str(user.uid),
            },
        }
    )


@auth_router.get(
    "/refresh-token",
    response_model=RefreshTokenResponseModel,
    status_code=status.HTTP_200_OK,
)
async def get_new_access_token(token_details: dict = Depends(refresh_token_bearer)):
    """Gets a new access token from a refresh token."""
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) <= datetime.now():
        raise InvalidToken()

    new_access_token = create_access_token(user_data=token_details["user"])

    return JSONResponse(
        content={
            "access_token": new_access_token,
        },
    )


@auth_router.get("/me", response_model=UserBooksModel, status_code=status.HTTP_200_OK)
async def get_current_logged_user(
    user=Depends(get_current_user),
    _: bool = Depends(role_checker),  # This restricts the endpoint for authorized users
):
    """Returns info about the current logged in user."""
    return user


@auth_router.get(
    "/logout",
    response_model=RevokeTokenResponseModel,
    status_code=status.HTTP_200_OK,
)
async def revoke_token(token_details: dict = Depends(access_token_bearer)):
    """Revokes a token to logout an user."""

    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(content={"message": "Logged out successfully!"})
