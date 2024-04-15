from asyncio import Event
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, cast

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

SESSION: Optional[Session] = None
SESSION_SET = Event()


def create_session(url: str):
    global SESSION
    engine = create_engine(url)
    SESSION = Session(engine)
    SESSION_SET.set()


@asynccontextmanager
async def current_session() -> AsyncGenerator[Session, None]:
    await SESSION_SET.wait()
    yield cast(Session, SESSION)
