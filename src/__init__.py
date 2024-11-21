"""
Main entrypoint for application.
"""

from fastapi import FastAPI

from src.books.routes import book_router

VERSION = "v1"

app = FastAPI(
    title="Bookly",
    version=VERSION,
    description="A REST API for a book review web service.",
)

app.include_router(book_router, prefix=f"/api/{VERSION}/books", tags=["books"])
