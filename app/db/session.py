from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().DB_URL
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    echo=get_settings().DB_DEBUG,
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False
)


@asynccontextmanager
async def get_session():
    session: Session = async_session()
    try:
        yield session
    finally:
        await session.close()

