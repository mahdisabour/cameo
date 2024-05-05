from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import IntegrityError

from app.core.config import get_settings
from app.util.exceptions import CustomDatabaseError

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


async def get_session():
    async with async_session() as session:
        try:
            yield session
        except IntegrityError as exc:
                await session.rollback()
                raise CustomDatabaseError(str(exc.orig))
        finally:
            await session.close()