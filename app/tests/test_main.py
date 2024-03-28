from fastapi.testclient import TestClient
import pytest

# API tests


@pytest.mark.usefixtures("db_setup")
def test_create_customer(client: TestClient):
    response = client.post(
        "/customers/",
        json={"first_name": "Anakin", "last_name": "Skywalker", "age": 42},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "first_name": "Anakin",
        "last_name": "Skywalker",
        "age": 42,
    }


@pytest.mark.usefixtures("db_setup")
def test_get_customer(client: TestClient):
    response = client.get("/customers/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "first_name": "Anakin",
        "last_name": "Skywalker",
        "age": 42,
    }


@pytest.mark.usefixtures("db_setup")
def test_create_item(client: TestClient):
    response = client.post(
        "/items/",
        json={
            "name": "Lightsaber",
            "description": "A real thing, not a toy!",
            "price": 1000.0,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Lightsaber",
        "description": "A real thing, not a toy!",
        "price": 1000.0,
    }


@pytest.mark.usefixtures("db_setup")
def test_list_items(client: TestClient):
    response = client.get("/items/")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Lightsaber",
            "description": "A real thing, not a toy!",
            "price": 1000.0,
        }
    ]
