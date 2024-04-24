# type: ignore


from typing import Optional

from pydantic import BaseModel, ConfigDict

from fastapi_do_zero.database.models import TaskStatus


class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    state: Optional[TaskStatus] = None


class TaskCreate(TaskBase):
    title: str
    description: str
    state: TaskStatus


class TaskUpdate(TaskBase):
    pass


class TaskInDBBase(TaskBase):
    id: int
    title: str
    description: str
    state: TaskStatus

    model_config = ConfigDict(from_attributes=True)


class Task(TaskInDBBase):
    pass


class TaskList(BaseModel):
    tasks: list[Task]
