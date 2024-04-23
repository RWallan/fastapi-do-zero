from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_do_zero.models import reg

ModelT = TypeVar("ModelT", bound=type(reg.mapped_as_dataclass))
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class BaseCRUD(Generic[CreateSchemaT, UpdateSchemaT]):
    def __init__(self, model) -> None:
        self.model = model

    async def create(self, session: AsyncSession, *, obj_in: CreateSchemaT):
        model_obj = self.model(**obj_in.model_dump())

        session.add(model_obj)
        await session.commit()
        await session.refresh(model_obj)

        return model_obj

    async def get_by_id(self, session: AsyncSession, *, id: int):
        obj = await session.scalar(
            select(self.model).where(self.model.id == id)
        )

        return obj

    async def read_multi(
        self, session: AsyncSession, *, skip: int, limit: int
    ):
        objs = await session.scalars(
            select(self.model).offset(skip).limit(limit)
        )

        return objs

    async def update(
        self, session: AsyncSession, *, db_obj, obj_in: UpdateSchemaT
    ):
        obj_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            setattr(db_obj, field, obj_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def delete(self, session: AsyncSession, *, db_obj):
        await session.delete(db_obj)
        await session.commit()
