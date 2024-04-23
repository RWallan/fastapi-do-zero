from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from fastapi_do_zero import crud, schemas
from fastapi_do_zero.helpers import deps
from fastapi_do_zero.helpers.security import JWT

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=schemas.Token)
async def access_token(
    form_data: deps.OAuth2Form,
    session: deps.Session,
):
    user = await crud.user.authenticate(
        session, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email ou senha incorreto",
        )

    access_token = JWT.encode(data={"sub": user.id})

    return schemas.Token(access_token=access_token, token_type="bearer")
