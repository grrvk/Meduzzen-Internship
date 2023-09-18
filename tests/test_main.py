from fastapi.testclient import TestClient


def test_health(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200