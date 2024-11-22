"""
Routes for the books module.
"""

from typing import List

import uuid
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.schemas import Book, BookCreateModel, BookUpdateModel
from src.db.main import get_session
from src.books.service import BookService

book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    """Lists existing books."""
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session)
) -> dict:
    """Creates a new book."""
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_uid}", response_model=Book)
async def get_book(
    book_uid: uuid.UUID, session: AsyncSession = Depends(get_session)
) -> dict:
    """Returns a specific book by its ID."""
    book = await book_service.get_book(book_uid, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found."
        )
    return book


@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(
    book_uid: uuid.UUID,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Updates a specific book by its ID."""
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found."
        )
    return updated_book


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    """Deletes a specific book by its ID."""
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return {}
