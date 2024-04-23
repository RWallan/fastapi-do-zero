import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from fastapi_do_zero.app import app
from fastapi_do_zero.database import get_session
from fastapi_do_zero.models import User, reg


@pytest_asyncio.fixture
async def client(session):
    def get_session_override():
        return session

    async with AsyncClient(
        app=app, base_url="http://127.0.0.1:8000"
    ) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Session = async_sessionmaker(bind=engine)
    async with engine.begin() as conn:
        await conn.run_sync(reg.metadata.create_all)

    yield Session()

    async with engine.begin() as conn:
        await conn.run_sync(reg.metadata.drop_all)


@pytest_asyncio.fixture
async def user(session):
    user = User(username="teste", email="teste@teste.com", password="teste")
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
