from sqlalchemy import (
    String
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base_class import Base
from app.core.constant_variables import (
    STRING_LENGTH_32,
    STRING_LENGTH_64
) 


class BaseUser(Base):
    __tablename__ = "base_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        unique=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        unique=False,
        nullable=True
    )
    email: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        unique=True,
        nullable=True
    )
    phone_number: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        unique=True,
        nullable=True
    ) 
    avatar: Mapped[str] = mapped_column(String(STRING_LENGTH_32))

