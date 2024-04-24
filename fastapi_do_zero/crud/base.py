from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_do_zero.database.models import Task, User

ModelT = TypeVar("ModelT", User, Task)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class BaseCRUD(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    def __init__(self, model) -> None:
        self.model = model

    async def create(
        self, session: AsyncSession, *, obj_in: CreateSchemaT
    ) -> ModelT:
        model_obj = self.model(**obj_in.model_dump())

        session.add(model_obj)
        await session.commit()
        await session.refresh(model_obj)

        return model_obj

    async def get_by_id(
        self, session: AsyncSession, *, id: int
    ) -> Optional[ModelT]:
        obj = await session.scalar(
            select(self.model).where(self.model.id == id)
        )

        return obj

    async def read_multi(
        self, session: AsyncSession, *, skip: int, limit: int
    ) -> ScalarResult[Any]:
        objs = await session.scalars(
            select(self.model).offset(skip).limit(limit)
        )

        return objs

    async def update(
        self, session: AsyncSession, *, db_obj: ModelT, obj_in: UpdateSchemaT
    ) -> ModelT:
        obj_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            setattr(db_obj, field, obj_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def delete(self, session: AsyncSession, *, db_obj: ModelT) -> None:
        await session.delete(db_obj)
        await session.commit()
