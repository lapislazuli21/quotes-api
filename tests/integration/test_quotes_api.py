import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_quotes_public(client: TestClient):
    """
    Tests that the public GET endpoint is accessible without an API key.
    """
    response = client.get("/api/v1/quotes")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_quote_unauthorized(client: TestClient):
    """
    Tests that creating a quote fails with a 401 error if no API key is provided.
    """
    response = client.post("/api/v1/quotes", json={"content": "test", "author": 0})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_and_delete_quote_authorized(authorized_client: TestClient):
    """
    Tests the full lifecycle: creating, verifying, and deleting a quote
    using an authorized client.
    """

    # 1. Create a new quote
    new_quote_data = {"content": "The only thing we have to fear is fear itself.", "author": "FDR"}
    response = authorized_client.post("/api/v1/quotes", json=new_quote_data)

    assert response.status_code == 201
    created_quote = response.json()
    assert created_quote["content"] == new_quote_data["content"]
    assert "id" in created_quote
    quote_id = created_quote["id"]

    # 2. Verify the new quote can be retrieved
    response = authorized_client.get(f"/api/v1/quotes/{quote_id}")
    assert response.status_code == 200
    assert response.json()["id"] == quote_id

    # 3. Delete the quote
    response = authorized_client.delete(f"/api/v1/quotes/{quote_id}")
    assert response.status_code == 204

    # 4. Verify the quote is gone
    response = authorized_client.get(f"/api/v1/quotes/{quote_id}")
    assert response.status_code == 404