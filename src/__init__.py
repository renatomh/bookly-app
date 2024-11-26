"""
Main entrypoint for application.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.db.main import init_db
from src.auth.routes import auth_router
from src.books.routes import book_router


@asynccontextmanager
async def life_span(app: FastAPI):
    """Defines conde to run at the start of the application."""
    print("server is starting")
    await init_db()
    yield
    print("server has stopped")


VERSION = "v1"

app = FastAPI(
    title="Bookly",
    version=VERSION,
    description="A REST API for a book review web service.",
)

app.include_router(auth_router, prefix=f"/api/{VERSION}/auth", tags=["auth"])
app.include_router(book_router, prefix=f"/api/{VERSION}/books", tags=["books"])
