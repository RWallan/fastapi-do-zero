from typing import Any, Optional

from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_do_zero.crud.base import BaseCRUD
from fastapi_do_zero.database.models import Task
from fastapi_do_zero.schemas import TaskCreate, TaskUpdate


class TaskCRUD(BaseCRUD[Task, TaskCreate, TaskUpdate]):
    async def create(  # pyright: ignore
        self, session: AsyncSession, *, user_id: int, obj_in: TaskCreate
    ):
        task = self.model(**obj_in.model_dump(), user_id=user_id)

        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task

    async def query(
        self,
        session: AsyncSession,
        *,
        user_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        state: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100
    ) -> ScalarResult[Any]:
        query = select(self.model).where(self.model.user_id == user_id)

        if title:
            query = query.filter(self.model.title.contains(title))

        if description:
            query = query.filter(self.model.description.contains(description))

        if state:
            query = query.filter(self.model.state == state)

        tasks = await session.scalars(query.offset(offset).limit(limit))

        return tasks


task = TaskCRUD(Task)
