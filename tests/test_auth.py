from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_get_token(client, user):
    response = await client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token
