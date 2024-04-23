from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_do_zero.models import User
from fastapi_do_zero.schemas.user import UserCreate, UserUpdate

from .base import BaseCRUD


class UserCRUD(BaseCRUD[UserCreate, UserUpdate]):
    async def get_by_username(
        self, session: AsyncSession, *, username: str
    ) -> Optional[User]:
        user = await session.scalar(
            select(self.model).where(self.model.username == username)
        )

        return user


user = UserCRUD(User)
