import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_quotes_public(client: TestClient):
    """
    Tests that the public GET endpoint is accessible without an API key.
    """
    async for c in client:
        response = c.get("/api/v1/quotes")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_quote_unauthorized(client: TestClient):
    """
    Tests that creating a quote fails with a 401 error if no API key is provided.
    """
    async for c in client:
        response = c.post("/api/v1/quotes", json={"content": "test", "author": "test"})
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_and_delete_quote_authorized(authorized_client: TestClient):
    """
    Tests the full lifecycle: creating, verifying, and deleting a quote
    using an authorized client.
    """
    async for ac in authorized_client:
        # 1. Create a new quote
        new_quote_data = {"content": "The only thing we have to fear is fear itself.", "author": "FDR"}
        response = ac.post("/api/v1/quotes", json=new_quote_data)

        assert response.status_code == 201
        created_quote = response.json()
        assert created_quote["content"] == new_quote_data["content"]
        assert "id" in created_quote
        quote_id = created_quote["id"]

        # 2. Verify the new quote can be retrieved
        response = ac.get(f"/api/v1/quotes/{quote_id}")
        assert response.status_code == 200
        assert response.json()["id"] == quote_id

        # 3. Delete the quote
        response = ac.delete(f"/api/v1/quotes/{quote_id}")
        assert response.status_code == 204

        # 4. Verify the quote is gone
        response = ac.get(f"/api/v1/quotes/{quote_id}")
        assert response.status_code == 404