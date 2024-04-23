from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any
from zoneinfo import ZoneInfo

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_do_zero import crud
from fastapi_do_zero.database.init_session import get_session
from fastapi_do_zero.database.models import User
from fastapi_do_zero.helpers.settings import settings
from fastapi_do_zero.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class JWT:
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    @classmethod
    def encode(cls, data: dict[str, Any]):
        to_encode = data.copy()
        expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
            minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM
        )

        return encoded_jwt

    @classmethod
    def decode(cls, token: str) -> dict[str, Any]:
        return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])


class Hasher:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(
        cls, plain_password: str, hashed_password: str
    ) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = JWT.decode(token)

        token_data = TokenPayload(**payload)
    except (jwt.DecodeError, ValidationError):
        raise credentials_exception

    user = await crud.user.get_by_id(session, id=token_data.sub)

    if user is None:
        raise credentials_exception

    return user
