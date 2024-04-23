import pytest


@pytest.mark.asyncio
async def test_health_check(client):

    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "OK"}
