from http import HTTPStatus

import pytest

from fastapi_do_zero.schemas.user import User


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/users/",
        json={
            "username": "string",
            "password": "stringst",
            "email": "example@example.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "string",
        "email": "example@example.com",
        "id": 1,
    }


@pytest.mark.asyncio
async def test_create_duplicated_user(client, user):
    response = await client.post(
        "/users/",
        json={
            "username": "teste",
            "password": "stringst",
            "email": "example@example.com",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username já registrado"}


@pytest.mark.asyncio
async def test_read_users(client):
    response = await client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


@pytest.mark.asyncio
async def test_read_users_with_users(client, user):
    user_schema = User.model_validate(user).model_dump()
    response = await client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


@pytest.mark.asyncio
async def test_update_user(client, user):
    response = await client.put(
        "/users/1",
        json={
            "username": "string",
            "password": "stringst",
            "email": "example@example.com.br",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "string",
        "email": "example@example.com.br",
        "id": 1,
    }


@pytest.mark.asyncio
async def test_update_user_with_wrong_id(client):
    response = await client.put(
        "/users/2",
        json={
            "username": "string",
            "password": "stringst",
            "email": "example@example.com.br",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User não encontrado."}


@pytest.mark.asyncio
async def test_delete_user(client, user):
    response = await client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deletado."}


@pytest.mark.asyncio
async def test_delete_user_with_wrong_id(client):
    response = await client.delete("/users/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User não encontrado."}
