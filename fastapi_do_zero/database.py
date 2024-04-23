from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_do_zero.settings import settings

engine = create_async_engine(settings.DATABASE_URL)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
