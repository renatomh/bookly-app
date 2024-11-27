"""
Model schemas for the application.
"""

from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel
import uuid

from src.reviews.schemas import ReviewModel


class Book(BaseModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID]


class BookDetailModel(Book):
    reviews: List[ReviewModel]


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
