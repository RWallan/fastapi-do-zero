import pytest
from sqlalchemy import select

from fastapi_do_zero.database.models import Task, User


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = User(username="alice", password="secret", email="test@test.com")

    session.add(new_user)
    await session.commit()

    user = await session.scalar(select(User).where(User.username == "alice"))

    assert user.username == "alice"


@pytest.mark.asyncio
async def test_create_task(session, user):
    task = Task(
        title="Teste",
        description="Teste Desc",
        state="draft",  # pyright: ignore
        user_id=user.id,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    user = await session.scalar(select(User).where(User.id == user.id))

    assert task in user.tasks
