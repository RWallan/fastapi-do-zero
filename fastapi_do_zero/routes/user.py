from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_do_zero import crud, models, schemas
from fastapi_do_zero.database import get_session

router = APIRouter()


@router.post(
    "/users/", status_code=HTTPStatus.CREATED, response_model=schemas.User
)
async def create_user(
    user: schemas.UserCreate, session: AsyncSession = Depends(get_session)
) -> models.User:
    db_user = await crud.user.get_by_username(session, username=user.username)

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Username já registrado"
        )

    created_user = await crud.user.create(session, obj_in=user)
    return created_user


@router.get("/users/", response_model=schemas.UserList)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    users = await crud.user.read_multi(session, skip=skip, limit=limit)
    return {"users": users}


@router.put(
    "/users/{user_id}",
    status_code=HTTPStatus.CREATED,
    response_model=schemas.User,
)
async def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    session: AsyncSession = Depends(get_session),
):
    user_in_db = await crud.user.get_by_id(session, id=user_id)

    if not user_in_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User não encontrado."
        )

    updated_user = await crud.user.update(
        session, db_obj=user_in_db, obj_in=user
    )

    return updated_user


@router.delete("/users/{user_id}", response_model=schemas.Msg)
async def delete_user(
    user_id: int, session: AsyncSession = Depends(get_session)
):
    user_in_db = await crud.user.get_by_id(session, id=user_id)

    if not user_in_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User não encontrado."
        )

    await crud.user.delete(session, db_obj=user_in_db)

    return schemas.Msg(message="User deletado.")
