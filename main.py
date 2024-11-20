"""
Main entrypoint for application.
"""

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    """Root path/endpoint for the API."""
    return {"message": "Hello World!"}


@app.get("/greet")
async def greet_name(name: Optional[str] = "User", age: int = 0) -> dict:
    """Provides a greeting for the specified name."""
    return {"message": f"Hello, {name}!", "age": age}


class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post("/create-book")
async def create_book(book_data: BookCreateModel) -> dict:
    """Simple endpoint to showcase an object creation."""
    return {
        "title": book_data.title,
        "author": book_data.author,
    }
