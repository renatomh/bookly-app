"""Main database communication script."""

from sqlmodel import create_engine, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.config import Config

async_engine = AsyncEngine(
    create_engine(
        url=Config.database_url,
        echo=True,
    )
)


async def init_db():
    async with async_engine.begin() as conn:
        from src.books.models import Book

        # Creating all tables based on defined SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:  # type: ignore
    """Dependency to provide the session object."""
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with Session() as session:
        yield session
