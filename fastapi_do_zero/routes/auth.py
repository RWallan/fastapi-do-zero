from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_do_zero import crud, schemas
from fastapi_do_zero.database import get_session
from fastapi_do_zero.security import JWT

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
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
