import pytest
from sqlalchemy import select

from fastapi_do_zero.models.user import User


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = User(username="alice", password="secret", email="test@test.com")

    session.add(new_user)
    await session.commit()

    user = await session.scalar(select(User).where(User.username == "alice"))

    assert user.username == "alice"
