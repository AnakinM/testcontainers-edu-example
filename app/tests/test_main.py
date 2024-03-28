from fastapi.testclient import TestClient


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
