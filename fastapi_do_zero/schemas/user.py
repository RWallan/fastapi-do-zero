# type: ignore
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

UserPassword = Annotated[str, StringConstraints(min_length=8, max_length=64)]


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: UserPassword


class UserUpdate(UserBase):
    password: Optional[UserPassword] = None


class UserInDbBase(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class User(UserInDbBase): ...


class UserDb(UserInDbBase):
    password: Annotated[str, StringConstraints(min_length=8, max_length=65)]


class UserList(BaseModel):
    users: list[User]
