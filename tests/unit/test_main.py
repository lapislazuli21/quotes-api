from fastapi.testclient import TestClient

def test_read_root(client: TestClient):
    """
    Example test for a root endpoint.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    # This test will run with settings from .env.test because the 'client'
    # fixture from conftest.py is being used.
    # assert response.json()["env"] == "test"