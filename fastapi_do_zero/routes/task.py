from http import HTTPStatus

from fastapi import APIRouter

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
