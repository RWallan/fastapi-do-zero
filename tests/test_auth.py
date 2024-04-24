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


@pytest.mark.asyncio
async def test_token_inexistent_user(client):
    response = await client.post(
        "/auth/token",
        data={"username": "no_user@no_domain.com", "password": "teste"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email ou senha incorreto"}


@pytest.mark.asyncio
async def test_token_wrong_pwd(client, user):
    response = await client.post(
        "/auth/token",
        data={"username": user.email, "password": "wrong"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email ou senha incorreto"}


@pytest.mark.asyncio
async def test_refresh_token(client, token):
    response = await client.post(
        "/auth/refresh_token",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_token_expired_not_refresh(client, user):
    with freeze_time("2024-04-24 12:00:00"):
        response = await client.post(
            "/auth/token",
            data={"username": user.email, "password": user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2024-04-24 12:31:00"):

        response = await client.post(
            "/auth/refresh_token",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Não foi possível validar as credenciais"
    }
