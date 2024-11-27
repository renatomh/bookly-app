"""
Routes for the reviews module.
"""

from typing import List
import uuid

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import ReviewModel, ReviewCreateModel
from .service import ReviewService
from src.db.main import get_session
from src.db.models import User
from src.auth.dependencies import RoleChecker, get_current_user

review_router = APIRouter()
review_service = ReviewService()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@review_router.get(
    "/",
    response_model=List[ReviewModel],
    dependencies=[admin_role_checker],
)
async def get_all_reviews(session: AsyncSession = Depends(get_session)):
    """Lists existing reviews."""
    reviews = await review_service.get_all_reviews(session)

    return reviews


@review_router.get(
    "/{review_uid}", response_model=ReviewModel, dependencies=[user_role_checker]
)
async def get_review(
    review_uid: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    """Returns a specific review by its ID."""
    review = await review_service.get_review(review_uid, session)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found."
        )
    return review


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


@review_router.delete(
    "/{review_uid}",
    dependencies=[user_role_checker],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
    review_uid: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await review_service.delete_review_from_book(
        review_uid=review_uid,
        user_email=current_user.email,
        session=session,
    )

    return {}
