from http import HTTPStatus

import pytest
from freezegun import freeze_time


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


@pytest.mark.asyncio
async def test_token_expired_after_time(client, user):
    with freeze_time("2024-04-24 12:00:00"):
        response = await client.post(
            "/auth/token",
            data={"username": user.email, "password": user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2024-04-24 12:31:00"):
        response = await client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"username": "wrong", "email": "wrong@wrong.com"},
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Não foi possível validar as credenciais"
    }
