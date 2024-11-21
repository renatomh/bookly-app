"""
Main entrypoint for application.
"""

import json
from typing import List

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Books API",
    version="0.1.0",
    description="Simple CRUD API to manage books.",
)


class Book(BaseModel):
    id: int
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


# Loading books list
with open("books.json", "r") as f:
    books = json.load(f)


@app.get("/books", response_model=List[Book])
async def get_all_books():
    """Lists existing books."""
    return books


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: Book) -> dict:
    """Creates a new book."""
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book


@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int) -> dict:
    """Returns a specific book by its ID."""
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")


@app.patch("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    """Updates a specific book by its ID."""

    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """Deletes a specific book by its ID."""
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
