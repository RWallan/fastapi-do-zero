from __future__ import annotations

from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

reg = registry()


class TaskStatus(str, Enum):
    draft = "draft"
    todo = "todo"
    doing = "doing"
    done = "done"
    trash = "trash"


@reg.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]

    tasks: Mapped[list[Task]] = relationship(
        init=False,
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


@reg.mapped_as_dataclass
class Task:
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TaskStatus]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped[User] = relationship(
        init=False, back_populates="tasks", lazy="selectin"
    )
