"""
Model schemas for the application.
"""

from pydantic import BaseModel, Field
import uuid


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserLoginSimplifiedModel(BaseModel):
    email: str
    uid: uuid.UUID


class UserLoginResponseModel(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    user: UserLoginSimplifiedModel


class RefreshTokenResponseModel(BaseModel):
    access_token: str
