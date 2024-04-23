from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_do_zero.database.models import User
from fastapi_do_zero.helpers.security import Hasher
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

    async def get_by_email(
        self, session: AsyncSession, *, email: EmailStr
    ) -> Optional[User]:
        user = await session.scalar(
            select(self.model).where(self.model.email == email)
        )

        return user

    async def create(
        self, session: AsyncSession, *, obj_in: UserCreate
    ) -> User:
        hashed_obj_in = UserCreate(
            username=obj_in.username,
            email=obj_in.email,
            password=Hasher.get_password_hash(obj_in.password),
        )

        created_user = await super().create(session, obj_in=hashed_obj_in)

        return created_user

    async def update(
        self, session: AsyncSession, *, db_obj, obj_in: UserUpdate
    ) -> User:
        if obj_in.password:
            obj_in.password = Hasher.get_password_hash(obj_in.password)

        updated_user = await super().update(
            session, db_obj=db_obj, obj_in=obj_in
        )

        return updated_user

    async def authenticate(
        self, session: AsyncSession, *, email: EmailStr, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(session, email=email)

        if not user:
            return None

        if not Hasher.verify_password(password, user.password):
            return None

        return user


user = UserCRUD(User)
