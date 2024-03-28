import asyncio
from typing import AsyncGenerator, Generator
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from testcontainers.postgres import PostgresContainer  # type: ignore
from fastapi.testclient import TestClient
import pytest

from app.models import Base
from app.main import app
from app.schemas import CustomerCreate, ItemCreate

postgres = PostgresContainer(
    "postgres:16-alpine",
    username="anakin",
    password="anakin",
    dbname="testdb",
).with_bind_ports(5432, 5432)

unbound_postgres = PostgresContainer(
    "postgres:16-alpine",
    username="anakin",
    password="anakin",
    dbname="testdb",
)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def db_setup(request: pytest.FixtureRequest):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)

    engine = create_engine(postgres.get_connection_url())
    Base.metadata.create_all(engine)


@pytest_asyncio.fixture(scope="session")
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    unbound_postgres.start()
    connection_url = unbound_postgres.get_connection_url().replace(
        "postgresql+psycopg2", "postgresql+asyncpg"
    )
    engine = create_async_engine(connection_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()
    unbound_postgres.stop()


@pytest_asyncio.fixture(scope="session")
async def async_db(async_db_engine):
    AsyncSessionLocal = async_sessionmaker(async_db_engine, expire_on_commit=False)
    db = AsyncSessionLocal()

    yield db

    await db.close()


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_customer() -> CustomerCreate:
    return CustomerCreate(
        first_name="Anakin",
        last_name="Skywalker",
        age=42,
    )


@pytest.fixture
def sample_item() -> ItemCreate:
    return ItemCreate(
        name="Lightsaber",
        description="A real thing, not a toy!",
        price=1000.0,
    )
