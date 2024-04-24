from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_do_zero.crud.base import BaseCRUD
from fastapi_do_zero.database.models import Task
from fastapi_do_zero.schemas import TaskCreate, TaskUpdate


class TaskCRUD(BaseCRUD[TaskCreate, TaskUpdate]):
    async def create(  # pyright: ignore
        self, session: AsyncSession, *, user_id: int, obj_in: TaskCreate
    ):
        task = self.model(**obj_in.model_dump(), user_id=user_id)

        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task


task = TaskCRUD(Task)
