"""
Routes for the reviews module.
"""

import uuid
from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import ReviewModel, ReviewCreateModel
from .service import ReviewService
from src.db.main import get_session
from src.db.models import User
from src.auth.dependencies import get_current_user

review_router = APIRouter()
review_service = ReviewService()


@review_router.post(
    "/book/{book_uid}",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewModel,
)
async def add_review_to_books(
    book_uid: uuid.UUID,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Creates a new review for a book."""
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session,
    )

    return new_review
