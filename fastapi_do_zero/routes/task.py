from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query

from fastapi_do_zero import crud, schemas
from fastapi_do_zero.helpers import deps

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    session: deps.Session,
    current_user: deps.CurrentUser,
):
    task_in_db = await crud.task.create(
        session, user_id=current_user.id, obj_in=task
    )

    return task_in_db


# TODO: Testes
@router.get("/", response_model=schemas.TaskList)
async def list_tasks(
    session: deps.Session,
    current_user: deps.CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    tasks = await crud.task.query(
        session,
        user_id=current_user.id,
        title=title,
        description=description,
        state=state,
        offset=offset,
        limit=limit,
    )

    return {"tasks": tasks}


@router.put("/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: int,
    session: deps.Session,
    current_user: deps.CurrentUser,
    task: schemas.TaskUpdate,
):
    task_in_db = await crud.task.get_by_id(session, id=task_id)

    if not task_in_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Task não encontrada"
        )

    if task_in_db.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Sem permissão"
        )

    updated_task = await crud.task.update(
        session, db_obj=task_in_db, obj_in=task
    )

    return updated_task


@router.delete("/{task_id}", response_model=schemas.Msg)
async def delete_task(
    task_id: int, session: deps.Session, current_user: deps.CurrentUser
):
    task_in_db = await crud.task.get_by_id(session, id=task_id)

    if not task_in_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Task não encontrada"
        )

    if task_in_db.user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Sem permissão"
        )

    await crud.task.delete(session, db_obj=task_in_db)

    return schemas.Msg(message="Task deletada")
