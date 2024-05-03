from sqlalchemy import (
    String, 
    DateTime
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from app.db.base_class import Base
from app.core.constant_variables import (
    STRING_LENGTH_32,
    STRING_LENGTH_64
) 


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(STRING_LENGTH_32),
        unique=True,
    )
    name: Mapped[str | None] = mapped_column(
        String(STRING_LENGTH_32),
        unique=False,
    )
    email: Mapped[str | None] = mapped_column(
        String(STRING_LENGTH_32),
        unique=True,
    )
    phone_number: Mapped[str | None] = mapped_column(
        String(STRING_LENGTH_32),
    ) 
    date_of_birth: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
    )
    avatar: Mapped[str] = mapped_column(String(STRING_LENGTH_32))
    time_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    time_updated: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )
    user: Mapped["User"] = relationship(back_populates="account")
    talent: Mapped["Talent"] = relationship(back_populates="account")
    
