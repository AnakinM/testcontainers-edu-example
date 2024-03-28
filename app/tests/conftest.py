from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer  # type: ignore
from fastapi.testclient import TestClient
import pytest

from app.models import Base
from app.main import app

postgres = PostgresContainer(
    "postgres:16-alpine",
    username="anakin",
    password="anakin",
    dbname="testdb",
).with_bind_ports(5432, 5432)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def setup(request: pytest.FixtureRequest):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)

    engine = create_engine(postgres.get_connection_url())
    Base.metadata.create_all(engine)
    print("Database setup complete")
