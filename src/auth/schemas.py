"""
Model schemas for the application.
"""

from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
