from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from .models import Base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://anakin:anakin@localhost:5432/testdb"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)


@asynccontextmanager
async def async_db_session() -> AsyncGenerator[AsyncSession, None]:
    db = AsyncSessionLocal()
    try:
        yield db
    except Exception as e:
        await db.rollback()
        raise e
    finally:
        await db.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_db_session() as db:
        yield db


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
