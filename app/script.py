from testcontainers.postgres import PostgresContainer
import sqlalchemy

with PostgresContainer("postgres:16") as postgres:
    engine = sqlalchemy.create_engine(postgres.get_connection_url())
    with engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("select version()"))
        (version,) = result.fetchone()
