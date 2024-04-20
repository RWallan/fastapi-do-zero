import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from fastapi_do_zero.app import app
from fastapi_do_zero.models._base import reg


@pytest.fixture
def client():
    return TestClient(app)


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    Session = async_sessionmaker(bind=engine)
    async with engine.begin() as conn:
        await conn.run_sync(reg.metadata.create_all)

    yield Session()

    async with engine.begin() as conn:
        await conn.run_sync(reg.metadata.drop_all)
