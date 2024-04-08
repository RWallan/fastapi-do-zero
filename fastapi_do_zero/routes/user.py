from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from fastapi_do_zero import schemas

router = APIRouter()

database: list[schemas.UserDb] = []


@router.post(
    "/users/", status_code=HTTPStatus.CREATED, response_model=schemas.User
)
def create_user(user: schemas.UserCreate):
    created_user = schemas.UserDb(**user.model_dump(), id=len(database) + 1)
    database.append(created_user)
    return created_user


@router.get("/users/", response_model=schemas.UserList)
def read_users():
    return {"users": database}


@router.put(
    "/users/{user_id}",
    status_code=HTTPStatus.CREATED,
    response_model=schemas.User,
)
def update_user(user_id: int, user: schemas.UserUpdate):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User não encontrado."
        )

    retrieved_user = database[user_id - 1].model_dump()
    obj_data = user.model_dump(exclude_unset=True)
    updated_user = retrieved_user.copy()

    updated_user.update(obj_data)

    updated_user = schemas.UserDb(**updated_user)

    database[user_id - 1] = updated_user

    return updated_user


@router.delete("/users/{user_id}", response_model=schemas.Msg)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User não encontrado."
        )

    del database[user_id - 1]

    return schemas.Msg(message="User deletado.")
