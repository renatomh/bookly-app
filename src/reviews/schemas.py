"""
Model schemas for the application.
"""

from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    rating: int = Field(le=5)
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]


class ReviewCreateModel(BaseModel):
    rating: int = Field(le=5)
    review_text: str
