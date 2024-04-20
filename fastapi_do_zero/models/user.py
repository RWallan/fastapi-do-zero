from sqlalchemy.orm import Mapped, mapped_column

from ._base import reg


@reg.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
