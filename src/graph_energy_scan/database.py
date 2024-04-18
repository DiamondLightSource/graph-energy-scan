from asyncio import Event
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, cast

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

SESSION_MAKER: Optional[async_sessionmaker] = None
SESSION_CREATED = Event()


def create_session(url: str):
    global SESSION_MAKER
    engine = create_async_engine(url)
    SESSION_MAKER = async_sessionmaker(engine)
    SESSION_CREATED.set()


@asynccontextmanager
async def current_session() -> AsyncGenerator[AsyncSession, None]:
    await SESSION_CREATED.wait()
    async with cast(async_sessionmaker, SESSION_MAKER)() as session:
        yield session
