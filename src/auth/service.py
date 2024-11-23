"""
Service for authentication methods.
"""

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from .schemas import UserCreateModel
from .models import User
from .utils import generate_passwd_hash


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        return result.first()

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)

        return user is not None

    async def create_user(
        self, user_data: UserCreateModel, session: AsyncSession
    ) -> User:
        user_data_dict = user_data.model_dump()

        new_user = User(
            **user_data_dict,
        )

        new_user.password_hash = generate_passwd_hash(user_data_dict["password"])

        session.add(new_user)

        await session.commit()

        return new_user