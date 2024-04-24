from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_task(client, token):
    response = await client.post(
        "/task/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Teste",
            "description": "Teste Desc",
            "state": "draft",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "Teste",
        "description": "Teste Desc",
        "state": "draft",
    }
