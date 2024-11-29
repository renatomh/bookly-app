"""
Routes for the authentication module.
"""

from datetime import datetime

from fastapi import APIRouter, status, Depends, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_limiter.depends import RateLimiter

from .schemas import (
    UserModel,
    UserCreateModel,
    UserCreateResponseModel,
    UserLoginModel,
    UserLoginResponseModel,
    UserBooksModel,
    RefreshTokenResponseModel,
    RevokeTokenResponseModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from .service import UserService
from .utils import (
    create_access_token,
    verify_password,
    create_url_safe_token,
    decode_url_safe_token,
    generate_passwd_hash,
)
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    RoleChecker,
    get_current_user,
)
from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from src.errors import (
    UserAlreadyExists,
    InvalidCredentials,
    InvalidToken,
    UserNotFound,
    AccountNotVerified,
)
from src.config import Config
from src.celery_tasks import send_email

auth_router = APIRouter()
user_service = UserService()
refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()
# This will define routes allowed only for specified user roles
role_checker = RoleChecker(["admin", "user"])


@auth_router.post("/send-mail")
async def send_mail(emails: EmailModel):
    """Sends email to provided email addresses."""
    emails = emails.addresses

    html = "<h1>Welcome to the app</h1>"

    # Here, we're running a Celery task to send emails in background (with the '.delay' addition)
    send_email.delay(emails, "Welcome", html)

    return {"message": "Email sent successfully!"}


@auth_router.post(
    "/signup",
    response_model=UserCreateResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_account(
    user_data: UserCreateModel,
    bg_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    """Creates a new user account."""
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email.<p>
    """

    # Here, we're running a Celery task to send emails in background (with the '.delay' addition)
    send_email.delay([email], "Verify Your Email", html_message)

    return {
        "message": "Account Created! Check your email to verify the new account.",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    """Verifies an user email with the provided token."""

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully."},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "An error occured during verification."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


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

    if not user.is_verified:
        raise AccountNotVerified()

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


@auth_router.post(
    "/password-reset-request",
    dependencies=[Depends(RateLimiter(times=3, minutes=1))],
)
async def password_reset_request(email_data: PasswordResetRequestModel):
    """Sends an email to request password reset."""
    email = email_data.email

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset your Password</h1>
    <p>Please click this <a href="{link}">link</a> to reset your password.<p>
    """

    # Here, we're running a Celery task to send emails in background (with the '.delay' addition)
    send_email.delay([email], "Reset your Password", html_message)

    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password.",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    """Resets an user password from the provided token."""

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        new_password = passwords.new_password
        confirm_new_password = passwords.confirm_new_password

        if new_password != confirm_new_password:
            raise HTTPException(
                detail="Passwords don't match.", status_code=status.HTTP_400_BAD_REQUEST
            )

        passwd_hash = generate_passwd_hash(new_password)

        await user_service.update_user(user, {"password_hash": passwd_hash}, session)

        return JSONResponse(
            content={"message": "Password reset successfully."},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "An error occured during password reset."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
