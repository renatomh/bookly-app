"""
Routes for the books module.
"""

from typing import List

import uuid
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import Book, BookDetailModel, BookCreateModel, BookUpdateModel
from src.db.main import get_session
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])


@book_router.get("/", response_model=List[Book], dependencies=[Depends(role_checker)])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    """Lists existing books."""
    books = await book_service.get_all_books(session)
    return books


@book_router.get(
    "/user/{user_uid}", response_model=List[Book], dependencies=[Depends(role_checker)]
)
async def get_user_book_submissions(
    user_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    """Lists books submitted by a specific user."""
    books = await book_service.get_user_books(user_uid, session)
    return books


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[Depends(role_checker)],
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    """Creates a new book."""
    user_uid = token_details["user"]["user_uid"]
    new_book = await book_service.create_book(book_data, user_uid, session)
    return new_book


@book_router.get(
    "/{book_uid}", response_model=BookDetailModel, dependencies=[Depends(role_checker)]
)
async def get_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    """Returns a specific book by its ID."""
    book = await book_service.get_book(book_uid, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found."
        )
    return book


@book_router.patch(
    "/{book_uid}", response_model=Book, dependencies=[Depends(role_checker)]
)
async def update_book(
    book_uid: uuid.UUID,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    """Updates a specific book by its ID."""
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found."
        )
    return updated_book


@book_router.delete(
    "/{book_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(role_checker)],
)
async def delete_book(
    book_uid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    """Deletes a specific book by its ID."""
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return {}
