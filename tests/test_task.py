from http import HTTPStatus

import pytest

from fastapi_do_zero.database.models import Task, TaskStatus


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


@pytest.mark.asyncio
async def test_update_task(client, session, user, token):
    task = Task(
        title="teste",
        description="teste",
        state=TaskStatus.draft,
        user_id=user.id,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    response = await client.put(
        f"/task/{task.id}",
        json={"title": "teste!!"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "teste!!"


@pytest.mark.asyncio
async def test_delete_task(client, session, user, token):
    task = Task(
        title="teste",
        description="teste",
        state=TaskStatus.draft,
        user_id=user.id,
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    response = await client.delete(
        f"/task/{task.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Task deletada"
