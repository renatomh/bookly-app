"""
Main entrypoint for application.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from aioredis import Redis

from src.db.main import init_db
from src.auth.routes import auth_router
from src.books.routes import book_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from .errors import register_all_errors
from .middleware import register_middlware
from .config import Config


@asynccontextmanager
async def life_span(app: FastAPI):
    """Defines conde to run at the start of the application."""
    print("server is starting")

    # Initialize database
    await init_db()

    # Initialize FastAPILimiter with Redis
    redis = await Redis.from_url(
        f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis)

    yield
    print("server has stopped")


VERSION = "v1"

app = FastAPI(
    title="Bookly",
    version=VERSION,
    description="A REST API for a book review web service.",
    lifespan=life_span,
)

register_all_errors(app)

register_middlware(app)

app.include_router(auth_router, prefix=f"/api/{VERSION}/auth", tags=["auth"])
app.include_router(book_router, prefix=f"/api/{VERSION}/books", tags=["books"])
app.include_router(review_router, prefix=f"/api/{VERSION}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{VERSION}/tags", tags=["tags"])
