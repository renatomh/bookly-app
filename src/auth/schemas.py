"""
Model schemas for the application.
"""

from datetime import datetime
import uuid
from typing import List

from pydantic import BaseModel, Field

from src.books.schemas import Book
from src.reviews.schemas import ReviewModel


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)


class UserModel(BaseModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)


class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserLoginSimplifiedModel(BaseModel):
    email: str
    uid: uuid.UUID


class UserCreateResponseModel(BaseModel):
    message: str
    user: UserModel


class UserLoginResponseModel(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    user: UserLoginSimplifiedModel


class RefreshTokenResponseModel(BaseModel):
    access_token: str


class RevokeTokenResponseModel(BaseModel):
    message: str = "Logged out successfully!"


class EmailModel(BaseModel):
    addresses: List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str
