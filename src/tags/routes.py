"""
Routes for the tags module.
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import TagAddModel, TagCreateModel, TagModel
from .service import TagService
from src.auth.dependencies import RoleChecker
from src.books.schemas import Book
from src.db.main import get_session

tags_router = APIRouter()
tag_service = TagService()
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@tags_router.get(
    "/",
    response_model=List[TagModel],
    dependencies=[user_role_checker],
    status_code=status.HTTP_200_OK,
)
async def get_all_tags(session: AsyncSession = Depends(get_session)):
    """Get all existing tags."""
    tags = await tag_service.get_tags(session)

    return tags


@tags_router.post(
    "/",
    response_model=TagModel,
    status_code=status.HTTP_201_CREATED,
    dependencies=[user_role_checker],
)
async def add_tag(
    tag_data: TagCreateModel, session: AsyncSession = Depends(get_session)
) -> TagModel:
    """Creates a new tag."""

    tag_added = await tag_service.add_tag(tag_data=tag_data, session=session)

    return tag_added


@tags_router.post(
    "/book/{book_uid}/tags", response_model=Book, dependencies=[user_role_checker]
)
async def add_tags_to_book(
    book_uid: uuid.UUID,
    tag_data: TagAddModel,
    session: AsyncSession = Depends(get_session),
) -> Book:
    """Add tags to an existing book."""

    book_with_tag = await tag_service.add_tags_to_book(
        book_uid=book_uid, tag_data=tag_data, session=session
    )

    return book_with_tag


@tags_router.put(
    "/{tag_uid}", response_model=TagModel, dependencies=[user_role_checker]
)
async def update_tag(
    tag_uid: uuid.UUID,
    tag_update_data: TagCreateModel,
    session: AsyncSession = Depends(get_session),
) -> TagModel:
    """Updates an existing tag."""
    updated_tag = await tag_service.update_tag(tag_uid, tag_update_data, session)

    return updated_tag


@tags_router.delete(
    "/{tag_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[user_role_checker],
)
async def delete_tag(
    tag_uid: uuid.UUID, session: AsyncSession = Depends(get_session)
) -> None:
    """Deletes an existing tag."""
    await tag_service.delete_tag(tag_uid, session)

    return {}
