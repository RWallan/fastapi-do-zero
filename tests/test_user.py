from http import HTTPStatus


def test_create_user(client):
    response = client.post(
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


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "string",
                "email": "example@example.com",
                "id": 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
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


def test_update_user_with_wrong_id(client):
    response = client.put(
        "/users/2",
        json={
            "username": "string",
            "password": "stringst",
            "email": "example@example.com.br",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User não encontrado."}


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deletado."}


def test_delete_user_with_wrong_id(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User não encontrado."}
